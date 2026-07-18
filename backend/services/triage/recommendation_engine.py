from typing import List, Dict, Any
from services.triage.medical_knowledge_base import MedicalKnowledgeBase

class RecommendationEngine:

    @classmethod
    def determine_care_level(cls, severity: str, possible_diseases: List[Dict[str, Any]]) -> str:
        """
        Maps severity and predicted diseases to a care level (home | clinic | urgent | emergency).
        """
        # Check if any suspected disease demands an emergency or urgent level
        highest_disease_care = "home"
        care_hierarchy = {"home": 0, "clinic": 1, "urgent": 2, "emergency": 3}

        for d in possible_diseases:
            name = d.get("name")
            kb_details = MedicalKnowledgeBase.get_condition_details(name)
            if kb_details:
                d_care = kb_details.get("care_level", "home")
                if care_hierarchy.get(d_care, 0) > care_hierarchy.get(highest_disease_care, 0):
                    highest_disease_care = d_care

        # Check severity mapping
        severity_care = "home"
        if severity == "high":
            severity_care = "emergency"
        elif severity == "moderate":
            severity_care = "urgent"
        elif severity == "mild":
            severity_care = "clinic"

        # Return the highest care level required
        if care_hierarchy.get(highest_disease_care, 0) > care_hierarchy.get(severity_care, 0):
            return highest_disease_care
        return severity_care

    @classmethod
    def get_recommended_tests(cls, possible_diseases: List[Dict[str, Any]]) -> List[str]:
        """
        Gathers diagnostic tests from the knowledge base for predicted diseases.
        """
        tests = []
        for d in possible_diseases:
            name = d.get("name")
            kb_details = MedicalKnowledgeBase.get_condition_details(name)
            if kb_details:
                for test in kb_details.get("recommended_tests", []):
                    if test not in tests:
                        tests.append(test)
        
        # Default safety tests if list is empty
        if not tests:
            tests = ["Routine Blood Test (CBC)", "Primary Clinical Evaluation"]
            
        return tests

    @classmethod
    def get_supportive_advice(cls, possible_diseases: List[Dict[str, Any]], care_level: str) -> List[str]:
        """
        Retrieves supportive, non-prescriptive advice based on suspected conditions and care level.
        """
        advice = []
        
        # Grab specific advice from knowledge base
        for d in possible_diseases:
            name = d.get("name")
            kb_details = MedicalKnowledgeBase.get_condition_details(name)
            if kb_details:
                for adv in kb_details.get("supportive_advice", []):
                    if adv not in advice:
                        advice.append(adv)

        # Standard safety advice depending on care level
        if care_level == "emergency":
            advice.append("Call emergency services immediately.")
            advice.append("Do not engage in strenuous physical movement.")
        elif care_level == "urgent":
            advice.append("Seek immediate medical evaluation at an urgent care center or clinic.")
            advice.append("Keep a log of symptoms and temperature.")
        elif care_level == "clinic":
            advice.append("Schedule a visit with your primary healthcare provider.")
            advice.append("Ensure you get adequate rest and monitor for new or worsening symptoms.")
        else:
            advice.append("Stay well-hydrated with fluids.")
            advice.append("Get plenty of rest.")
            advice.append("Monitor temperature and fever regularly.")

        # Ensure no prescriptive drug names are suggested (safety constraint)
        filtered_advice = []
        medication_blacklist = ["aspirin", "ibuprofen", "paracetamol", "antibiotic", "acetaminophen"]
        for item in advice:
            # Check if any blacklisted drug is mentioned and rephrase or skip
            contains_drug = False
            for drug in medication_blacklist:
                if drug in item.lower():
                    contains_drug = True
                    break
            if not contains_drug:
                filtered_advice.append(item)

        # Add general medical disclaimer
        filtered_advice.append("Disclaimer: This is supportive advice only, not a formal medical prescription. Always consult a licensed physician.")
        
        return filtered_advice
