import re
from typing import List, Dict

class SymptomExtractor:
    # Maps common colloquial phrases to standardized clinical terms
    SYMPTOM_MAP = {
        "pee burns": "burning urination",
        "burning urination": "burning urination",
        "pain when urinating": "burning urination",
        "burning sensation while urinating": "burning urination",
        "burning sensation when urinating": "burning urination",
        "hurts to pee": "burning urination",
        "painful urination": "burning urination",
        "stinging urination": "burning urination",
        
        "hurts when i swallow": "sore throat",
        "painful swallowing": "sore throat",
        "sore throat": "sore throat",
        "throat hurts": "sore throat",
        "swallowing pain": "sore throat",
        
        "cannot catch my breath": "shortness of breath",
        "can't catch my breath": "shortness of breath",
        "shortness of breath": "shortness of breath",
        "trouble breathing": "shortness of breath",
        "difficulty breathing": "shortness of breath",
        "gasps for air": "shortness of breath",
        "gasping for air": "shortness of breath",
        "heavy breathing": "shortness of breath",
        
        "chest feels heavy": "chest pain",
        "heavy chest": "chest pain",
        "chest pain": "chest pain",
        "chest tightness": "chest pain",
        "tightness in chest": "chest pain",
        "chest pressure": "chest pain",
        "chest hurts": "chest pain",
        "pain in chest": "chest pain",
        "crushing chest pain": "chest pain",
        "pressure in my chest": "chest pain",
        "chest feels tight": "chest pain",
        
        "pain in left arm": "left arm pain",
        "left arm pain": "left arm pain",
        "arm pain": "left arm pain",
        
        "sweating": "sweating",
        "perspiring": "sweating",
        "excessive sweating": "sweating",
        
        "high fever": "high fever",
        "fever": "fever",
        "running a fever": "fever",
        "hot forehead": "fever",
        
        "rash": "rash",
        "skin rash": "rash",
        "red spots": "rash",
        
        "joint pain": "joint pain",
        "achy joints": "joint pain",
        "pain in joints": "joint pain",
        
        "pain behind eyes": "pain behind eyes",
        "retro-orbital pain": "pain behind eyes",
        "eyes hurt behind": "pain behind eyes",
        "pain behind eye": "pain behind eyes",
        
        "abdominal pain": "abdominal pain",
        "stomach pain": "abdominal pain",
        "pain in stomach": "abdominal pain",
        "stomach hurts": "abdominal pain",
        "stomach cramps": "abdominal pain",
        
        "right lower quadrant": "right lower quadrant pain",
        "rlq pain": "right lower quadrant pain",
        "pain in right lower stomach": "right lower quadrant pain",
        "pain in right lower abdomen": "right lower quadrant pain",
        
        "loss of appetite": "loss of appetite",
        "not hungry": "loss of appetite",
        "unable to eat": "loss of appetite",
        
        "cloudy urine": "cloudy urine",
        "urine looks cloudy": "cloudy urine",
        
        "frequent urination": "frequent urination",
        "need to pee constantly": "frequent urination",
        "urinating frequently": "frequent urination",
        "going to bathroom frequently": "frequent urination",
        "pee frequently": "frequent urination",
        
        "sudden numbness": "sudden numbness",
        "numbness": "sudden numbness",
        "numbness in face": "sudden numbness",
        "numbness in arm": "sudden numbness",
        "numbness in leg": "sudden numbness",
        
        "slurred speech": "slurred speech",
        "difficulty speaking": "slurred speech",
        "cannot speak clearly": "slurred speech",
        
        "headache": "headache",
        "severe headache": "severe headache",
        "stiff neck": "stiff neck",
        
        "coughing up blood": "coughing up blood",
        "coughing blood": "coughing up blood",
        "blood in phlegm": "coughing up blood",
        
        "unconscious": "loss of consciousness",
        "passed out": "loss of consciousness",
        "lost consciousness": "loss of consciousness",
        "fainted": "loss of consciousness",
        "unresponsive": "loss of consciousness",
        
        "heavy bleeding": "heavy bleeding",
        "bleeding heavily": "heavy bleeding",
        "pulsing bleeding": "heavy bleeding",
        
        "seizure": "seizure",
        "convulsion": "seizure",
        "seizures": "seizure",
        
        "severe allergic reaction": "severe allergic reaction",
        "anaphylaxis": "severe allergic reaction",
        "swelling of face": "severe allergic reaction",
        
        "blue lips": "blue lips",
        "lips turned blue": "blue lips",
        
        "severe burns": "severe burns",
        "major trauma": "major trauma",
        
        "cough": "cough",
        "coughing": "cough",
        "runny nose": "runny nose",
        "sneezing": "sneezing",
        "vomiting": "vomiting",
        "nausea": "nausea",
        "dizziness": "dizziness",
        "fatigue": "fatigue",
        "body pain": "body pain",
        "body aches": "body aches",
        "body ache": "body aches",
        "muscle pain": "muscle pain",
        "sore muscles": "muscle pain",
        "wheezing": "wheezing",
        "excessive thirst": "excessive thirst",
        "blurry vision": "blurry vision",
        "back pain": "back pain",
        "side pain": "back pain",
        "flank pain": "back pain"
    }

    @classmethod
    def extract_symptoms(cls, text: str) -> List[str]:
        """
        Extracts and normalizes clinical symptoms from raw natural language input.
        """
        text_lower = text.lower()
        extracted = []
        for phrase, clinical_symptom in cls.SYMPTOM_MAP.items():
            # Use basic pattern matching or word searches
            # Look for exact match or word boundaries where appropriate
            pattern = r'\b' + re.escape(phrase) + r'\b'
            if re.search(pattern, text_lower) or phrase in text_lower:
                if clinical_symptom not in extracted:
                    extracted.append(clinical_symptom)
        return extracted
