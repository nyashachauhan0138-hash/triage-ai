from typing import List, Dict, Any

class FollowupGenerator:
    # Explicit mapping of follow-up questions for specific clinical conditions
    FOLLOWUP_QUESTIONS = {
        "Urinary Tract Infection": "Do you have fever, chills, or pain in your back or sides?",
        "Appendicitis": "Did the abdominal pain start near your belly button and move to the right side?",
        "Dengue": "Have you noticed any skin rash, bleeding gums, or severe muscle/joint pain?",
        "Pneumonia": "Are you coughing up mucus, and if so, what color is it?",
        "Myocardial Infarction": "Are you experiencing pain in your left arm, jaw, neck, or back, or cold sweats?",
        "Stroke": "Did the numbness or weakness occur suddenly, and are you having trouble with speech?",
        "Kidney Stones": "Is the back pain sudden and severe, and have you noticed any blood in your urine?",
        "Migraine": "Is the headache throbbing, on one side of your head, and accompanied by sensitivity to light or sound?",
        "Diabetes": "Have you noticed sudden changes in weight, extreme hunger, or frequent infections that heal slowly?",
        "Asthma Exacerbation": "Are you experiencing wheezing, chest tightness, or difficulty talking in full sentences?"
    }

    @classmethod
    def generate_followup(
        cls, 
        possible_diseases: List[Dict[str, Any]], 
        confidence: float, 
        current_symptoms: List[str],
        llm_question: str = ""
    ) -> Dict[str, Any]:
        """
        Generates one intelligent follow-up question if confidence is below 90% (0.90).
        If confidence is 90% or above, triage is complete.
        """
        # If confidence is 90% or higher, complete triage
        if confidence >= 0.90:
            return {
                "next_question": "",
                "triage_complete": True
            }

        # Check primary disease (highest confidence)
        if possible_diseases:
            primary_disease = possible_diseases[0]["name"]
            question = cls.FOLLOWUP_QUESTIONS.get(primary_disease)
            if question:
                return {
                    "next_question": question,
                    "triage_complete": False
                }

        # Fallback to dynamic LLM question if it was provided
        if llm_question and llm_question.strip():
            return {
                "next_question": llm_question.strip(),
                "triage_complete": False
            }

        # Default clinical question based on symptoms
        if "chest pain" in current_symptoms:
            q = "Does the chest pain radiate to your left arm or jaw, or are you experiencing sweating?"
        elif "fever" in current_symptoms:
            q = "Do you have any chills, body aches, joint pain, or rash?"
        else:
            q = "Are you experiencing any other symptoms, such as fever, nausea, or dizziness?"

        return {
            "next_question": q,
            "triage_complete": False
        }
