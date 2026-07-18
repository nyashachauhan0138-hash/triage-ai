from typing import List, Dict, Any
from services.triage.medical_knowledge_base import MedicalKnowledgeBase

class DiseasePredictor:

    @classmethod
    def predict_diseases(
        cls, 
        symptoms: List[str], 
        risk_factors: Dict[str, Any] = None,
        llm_predictions: List[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Predicts top 5 conditions based on symptoms, risk factors, and LLM guidance.
        """
        predictions = []
        risk_factors = risk_factors or {}
        llm_predictions = llm_predictions or []

        # 1. Generate rule-based predictions from the Medical Knowledge Base
        for cond_name, details in MedicalKnowledgeBase.CONDITIONS.items():
            cond_symptoms = details["symptoms"]
            cond_risk_factors = details["risk_factors"]
            
            # Count symptom matches
            matched_symptoms = [s for s in cond_symptoms if s in symptoms]
            if not matched_symptoms:
                continue
                
            symptom_match_ratio = len(matched_symptoms) / len(cond_symptoms)
            
            # Calculate risk factor boost
            risk_boost = 0.0
            for rf in cond_risk_factors:
                val = risk_factors.get(rf)
                if val is True or str(val).lower() in ["true", "yes", "1"]:
                    risk_boost += 0.1
                    
            # Base KB confidence
            kb_conf = min(symptom_match_ratio + risk_boost, 0.95)
            
            predictions.append({
                "name": cond_name,
                "confidence": kb_conf,
                "reason": details["explanation"],
                "source": "kb"
            })

        # 2. Merge with LLM predictions if present
        merged_predictions = {}
        
        # Populate with rule-based predictions first
        for p in predictions:
            merged_predictions[p["name"].lower()] = p

        # Merge LLM predictions
        for lp in llm_predictions:
            name = lp.get("name", "").strip()
            if not name:
                continue
            name_lower = name.lower()
            
            # Clean and normalize names
            matched_kb_name = None
            for kb_name in MedicalKnowledgeBase.CONDITIONS.keys():
                if kb_name.lower() in name_lower or name_lower in kb_name.lower():
                    matched_kb_name = kb_name
                    break
                    
            llm_conf = lp.get("confidence", 0.0)
            # Ensure confidence is float and handles percentages (e.g. 88 or 0.88)
            try:
                llm_conf = float(llm_conf)
                if llm_conf > 1.0:
                    llm_conf = llm_conf / 100.0
            except (ValueError, TypeError):
                llm_conf = 0.5
                
            reason = lp.get("reason", lp.get("explanation", ""))
            
            if matched_kb_name:
                kb_key = matched_kb_name.lower()
                if kb_key in merged_predictions:
                    # Average the KB match and LLM confidence
                    existing = merged_predictions[kb_key]
                    avg_conf = (existing["confidence"] * 0.4) + (llm_conf * 0.6)
                    existing["confidence"] = round(avg_conf, 2)
                    if reason:
                        existing["reason"] = reason
                else:
                    kb_details = MedicalKnowledgeBase.CONDITIONS[matched_kb_name]
                    merged_predictions[kb_key] = {
                        "name": matched_kb_name,
                        "confidence": round(llm_conf, 2),
                        "reason": reason or kb_details["explanation"],
                        "source": "llm_kb_match"
                    }
            else:
                # Store new disease predicted by LLM
                merged_predictions[name_lower] = {
                    "name": name,
                    "confidence": round(llm_conf, 2),
                    "reason": reason or f"Symptoms suggest a possible case of {name}.",
                    "source": "llm_only"
                }

        # Convert to list and sort by confidence descending
        final_list = list(merged_predictions.values())
        final_list.sort(key=lambda x: x["confidence"], reverse=True)

        # Take Top 5
        top_5 = final_list[:5]

        # Standardize naming and reasoning to ensure safe language
        formatted_top_5 = []
        for item in top_5:
            name = item["name"]
            conf = item["confidence"]
            reason = item["reason"]
            
            # Ensure we do not claim confirmed diagnoses
            if "suggests" not in reason.lower() and "possible" not in reason.lower() and "likely" not in reason.lower():
                reason = f"Symptoms may suggest {name}. {reason}"
                
            formatted_top_5.append({
                "name": name,
                "confidence": conf,
                "reason": reason
            })

        # Determine highest confidence
        max_conf = formatted_top_5[0]["confidence"] if formatted_top_5 else 0.0

        # If no diseases predicted, add a default fallback
        if not formatted_top_5 and symptoms:
            formatted_top_5.append({
                "name": "Undetermined Condition",
                "confidence": 0.5,
                "reason": "The symptoms provided require further diagnostic information to classify."
            })
            max_conf = 0.5

        return {
            "possible_diseases": formatted_top_5,
            "top_confidence": max_conf
        }
