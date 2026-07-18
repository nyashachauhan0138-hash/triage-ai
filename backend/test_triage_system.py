import sys
import os
from pathlib import Path

# Automatically re-execute using the project's virtual environment if run with system python
try:
    import fastapi
    import pydantic
except ImportError:
    script_dir = Path(__file__).resolve().parent
    venv_python = (script_dir.parent.parent / ".venv" / "bin" / "python").absolute()
    if venv_python.exists() and Path(sys.executable).absolute() != venv_python:
        print(f"Required libraries not found in current environment. Re-running script using virtualenv python: {venv_python}")
        os.execv(str(venv_python), [str(venv_python)] + sys.argv)
    else:
        print("Error: Missing required packages.")
        sys.exit(1)

import unittest
from services.triage.symptom_extractor import SymptomExtractor
from services.triage.emergency_detector import EmergencyDetector
from services.triage.severity_predictor import SeverityPredictor
from services.triage.disease_predictor import DiseasePredictor
from services.triage.recommendation_engine import RecommendationEngine
from services.triage.followup_generator import FollowupGenerator
from services.triage.triage_coordinator import TriageCoordinator
from models.chat import Message

class TestTriageSystem(unittest.TestCase):

    def test_symptom_extractor_spelling_and_synonyms(self):
        """
        Tests Goal 1: Extracted symptoms from conversational/colloquial text.
        """
        # Test "My pee burns." -> burning urination
        s1 = SymptomExtractor.extract_symptoms("My pee burns.")
        self.assertIn("burning urination", s1)

        # Test "It hurts when I swallow." -> sore throat
        s2 = SymptomExtractor.extract_symptoms("It hurts when I swallow.")
        self.assertIn("sore throat", s2)

        # Test "My chest feels heavy." -> chest pain
        s3 = SymptomExtractor.extract_symptoms("My chest feels heavy.")
        self.assertIn("chest pain", s3)

        # Test "I cannot catch my breath." -> shortness of breath
        s4 = SymptomExtractor.extract_symptoms("I cannot catch my breath.")
        self.assertIn("shortness of breath", s4)

        # Test spelling mistakes / abbreviations
        s5 = SymptomExtractor.extract_symptoms("i have rlq pain and stomach hurts")
        self.assertIn("right lower quadrant pain", s5)
        self.assertIn("abdominal pain", s5)

    def test_emergency_detection(self):
        """
        Tests Goal 4: Immediate emergency rules engine bypass.
        """
        # crushing chest pain -> Emergency
        self.assertTrue(EmergencyDetector.check_emergency(["chest pain"], "I am experiencing crushing chest pain"))
        
        # passed out -> Emergency
        self.assertTrue(EmergencyDetector.check_emergency(["loss of consciousness"]))

        # minor cold symptoms -> Not Emergency
        self.assertFalse(EmergencyDetector.check_emergency(["cough", "runny nose"]))

    def test_severity_prediction(self):
        """
        Tests Goal 3: Severity score mapping (low, mild, moderate, high).
        """
        # Critical case (chest pain + short of breath)
        sev1 = SeverityPredictor.predict_severity(
            symptoms=["chest pain", "shortness of breath"],
            emergency_flag=True
        )
        self.assertEqual(sev1["severity"], "high")
        self.assertEqual(sev1["severity_score"], 10.0)

        # Moderate case (fever + joint pain)
        sev2 = SeverityPredictor.predict_severity(
            symptoms=["fever", "joint pain"],
            emergency_flag=False
        )
        self.assertEqual(sev2["severity"], "mild")  # 3.8 score
        
        # High case (high fever + stiff neck + abdominal pain)
        sev3 = SeverityPredictor.predict_severity(
            symptoms=["high fever", "stiff neck", "abdominal pain"],
            emergency_flag=False
        )
        self.assertIn(sev3["severity"], ["moderate", "high"])

    def test_disease_prediction_ranking_and_confidence(self):
        """
        Tests Goal 2 & 6: Top 5 conditions and confidence limits.
        """
        # Symptoms indicating Dengue (high fever, pain behind eyes, rash, joint pain)
        symptoms = ["high fever", "pain behind eyes", "rash", "joint pain"]
        res = DiseasePredictor.predict_diseases(symptoms=symptoms)
        possible_diseases = res["possible_diseases"]
        
        # Check that Dengue is predicted as the top disease
        self.assertTrue(len(possible_diseases) > 0)
        self.assertEqual(possible_diseases[0]["name"], "Dengue")
        self.assertTrue(possible_diseases[0]["confidence"] > 0.60)

        # Test confidence below 60% guardrail
        res_low = DiseasePredictor.predict_diseases(symptoms=["fatigue"])
        self.assertTrue(res_low["top_confidence"] < 0.60)

    def test_recommendations(self):
        """
        Tests Goal 10, 11, 12: Recommended tests, care level and safety advice.
        """
        diseases = [{"name": "Urinary Tract Infection", "confidence": 0.85, "reason": "test"}]
        
        # Care Level UTI -> clinic
        care = RecommendationEngine.determine_care_level("mild", diseases)
        self.assertEqual(care, "clinic")

        # Recommended Tests UTI -> Urinalysis, Urine Culture
        tests = RecommendationEngine.get_recommended_tests(diseases)
        self.assertIn("Urinalysis", tests)
        self.assertIn("Urine Culture", tests)

        # Medication Advice (No prescriptions, general rest/water advice)
        advice = RecommendationEngine.get_supportive_advice(diseases, care)
        self.assertTrue(any("water" in a.lower() or "hydrated" in a.lower() for a in advice))
        
        # Ensure no actual antibiotic names are output
        self.assertFalse(any("ciprofloxacin" in a.lower() or "amoxicillin" in a.lower() for a in advice))

    def test_dynamic_followup_question(self):
        """
        Tests Goal 5: Dynamic follow-up question triggers if confidence < 90%.
        """
        diseases = [{"name": "Urinary Tract Infection", "confidence": 0.85, "reason": "test"}]
        
        # Confidence 85% -> should generate next question
        f1 = FollowupGenerator.generate_followup(diseases, 0.85, ["burning urination"])
        self.assertFalse(f1["triage_complete"])
        self.assertIn("fever", f1["next_question"].lower())

        # Confidence 95% -> Triage complete
        f2 = FollowupGenerator.generate_followup(diseases, 0.95, ["burning urination"])
        self.assertTrue(f2["triage_complete"])
        self.assertEqual(f2["next_question"], "")

    def test_contradictory_and_empty_inputs(self):
        """
        Tests contradictory symptoms and empty inputs.
        """
        # Empty input should default gracefully
        symptoms = SymptomExtractor.extract_symptoms("")
        self.assertEqual(len(symptoms), 0)

        # Contradictory symptoms (e.g. runny nose but crushing chest pain)
        # Should flag emergency because of crushing chest pain
        emergency = EmergencyDetector.check_emergency(["cough", "crushing chest pain"])
        self.assertTrue(emergency)

if __name__ == "__main__":
    unittest.main()
