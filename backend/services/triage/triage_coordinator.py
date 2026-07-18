import json
from typing import List, Dict, Any
from services.groq_service import GroqService
from utils.helpers import extract_json

from services.triage.symptom_extractor import SymptomExtractor
from services.triage.emergency_detector import EmergencyDetector
from services.triage.severity_predictor import SeverityPredictor
from services.triage.disease_predictor import DiseasePredictor
from services.triage.recommendation_engine import RecommendationEngine
from services.triage.followup_generator import FollowupGenerator

class TriageCoordinator:

    @classmethod
    def triage(
        cls, 
        messages: List[Any], 
        vitals: Dict[str, Any] = None, 
        voice: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Coordinates the entire triage pipeline.
        """
        # 1. Fetch natural language logs
        last_message = messages[-1].content if messages else ""
        full_text = " ".join([m.content for m in messages])

        # 2. Query the LLM to get clinical extraction and estimates
        raw_llm_response = GroqService.generate(messages)
        extracted_data = extract_json(raw_llm_response)

        # 3. Symptom Extraction
        llm_symptoms = extracted_data.get("extracted_symptoms", [])
        local_symptoms = SymptomExtractor.extract_symptoms(full_text)
        
        # Merge symptoms safely
        symptoms_set = set()
        for s in llm_symptoms + local_symptoms:
            s_clean = s.strip().lower()
            if s_clean:
                symptoms_set.add(s_clean)
        combined_symptoms = list(symptoms_set)

        # Body regions
        body_regions = extracted_data.get("body_regions", [])
        if not body_regions:
            # Fallback parsing of regions from text
            body_regions = []
            regions = ["chest", "abdomen", "head", "throat", "urinary", "arm", "leg", "face", "back", "groin", "skin", "joints"]
            for r in regions:
                if r in full_text.lower():
                    body_regions.append(r)

        # 4. Emergency Detection
        emergency_flag = EmergencyDetector.check_emergency(combined_symptoms, full_text)

        # 5. Risk Factors
        risk_factors = extracted_data.get("risk_factors", {})
        # If not present, try parsing from text
        if not risk_factors:
            risk_factors = {
                "age": None,
                "pregnancy": "pregnant" in full_text.lower(),
                "diabetes": "diabet" in full_text.lower(),
                "hypertension": "hypertension" in full_text.lower() or "high blood pressure" in full_text.lower(),
                "asthma": "asthma" in full_text.lower(),
                "smoking": "smok" in full_text.lower()
            }

        # 6. Disease Prediction
        llm_diseases = extracted_data.get("possible_diseases", [])
        prediction_results = DiseasePredictor.predict_diseases(
            symptoms=combined_symptoms,
            risk_factors=risk_factors,
            llm_predictions=llm_diseases
        )
        possible_diseases = prediction_results["possible_diseases"]
        top_confidence = prediction_results["top_confidence"]

        # 7. Severity Prediction
        severity_results = SeverityPredictor.predict_severity(
            symptoms=combined_symptoms,
            emergency_flag=emergency_flag,
            vitals=vitals,
            voice=voice,
            risk_factors=risk_factors
        )
        severity_score = severity_results["severity_score"]
        severity = severity_results["severity"]

        # 8. Recommendation Engine
        care_level = RecommendationEngine.determine_care_level(severity, possible_diseases)
        recommended_tests = RecommendationEngine.get_recommended_tests(possible_diseases)
        supportive_advice = RecommendationEngine.get_supportive_advice(possible_diseases, care_level)

        # 9. Follow-up Question
        llm_question = extracted_data.get("next_question", "")
        followup_results = FollowupGenerator.generate_followup(
            possible_diseases=possible_diseases,
            confidence=top_confidence,
            current_symptoms=combined_symptoms,
            llm_question=llm_question
        )
        next_question = followup_results["next_question"]
        triage_complete = followup_results["triage_complete"]

        # 10. Format User Message
        # If highest confidence is below 60%, do NOT make a definitive prediction.
        if top_confidence < 0.60:
            message = "More information is needed."
        else:
            if emergency_flag or care_level == "emergency":
                message = "Emergency alert: Your symptoms may indicate a critical condition. Please seek immediate emergency medical care."
            else:
                primary_disease = possible_diseases[0]["name"] if possible_diseases else "an undetermined condition"
                message = f"Based on your symptoms, a possible condition is {primary_disease}. General advice: " + ", ".join(supportive_advice[:2]) + "."

        summary = extracted_data.get("summary", "")
        if not summary:
            summary = f"Patient presented symptoms: {', '.join(combined_symptoms)}. Severity score: {severity_score} ({severity})."

        return {
            "message": message,
            "extracted_symptoms": combined_symptoms,
            "body_regions": body_regions,
            "severity_score": severity_score,
            "severity": severity,
            "care_level": care_level,
            "emergency_flag": emergency_flag,
            "possible_diseases": possible_diseases,
            "recommended_tests": recommended_tests,
            "next_question": next_question,
            "triage_complete": triage_complete,
            "summary": summary,
            "confidence": round(top_confidence, 2)
        }
