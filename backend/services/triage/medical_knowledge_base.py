from typing import Dict, Any, List

class MedicalKnowledgeBase:
    # A database of common conditions with their clinical characteristics
    CONDITIONS: Dict[str, Dict[str, Any]] = {
        "Myocardial Infarction": {
            "symptoms": ["chest pain", "left arm pain", "sweating", "shortness of breath", "chest pressure", "chest tightness"],
            "risk_factors": ["diabetes", "hypertension", "smoking", "age", "hyperlipidemia", "cardiac history"],
            "base_severity": 10,
            "care_level": "emergency",
            "recommended_tests": ["Electrocardiogram (ECG)", "Cardiac Troponin Test", "Echocardiogram", "Chest X-Ray"],
            "explanation": "Chest pain/pressure, left arm pain, sweating, and shortness of breath collectively suggest a potential myocardial infarction (heart attack).",
            "supportive_advice": [
                "Sit down and remain completely calm.",
                "Do not engage in physical activity.",
                "Seek immediate emergency medical help.",
                "If prescribed, take baby aspirin if advised by emergency operators."
            ]
        },
        "Stroke": {
            "symptoms": ["sudden numbness", "slurred speech", "difficulty speaking", "weakness in arm", "weakness in leg", "facial droop"],
            "risk_factors": ["hypertension", "diabetes", "smoking", "age", "cardiac history"],
            "base_severity": 10,
            "care_level": "emergency",
            "recommended_tests": ["CT Scan of the Brain", "MRI of the Brain", "Carotid Ultrasound"],
            "explanation": "Sudden onset of slurred speech, facial droop, or weakness/numbness on one side of the body suggests a possible acute stroke.",
            "supportive_advice": [
                "Note the exact time symptoms started.",
                "Do not take aspirin or other blood thinners.",
                "Seek immediate emergency medical services (time is brain)."
            ]
        },
        "Anaphylaxis": {
            "symptoms": ["severe allergic reaction", "swelling of face", "difficulty swallowing", "difficulty breathing", "hives", "wheezing"],
            "risk_factors": ["allergies", "asthma"],
            "base_severity": 10,
            "care_level": "emergency",
            "recommended_tests": ["Clinical Evaluation", "Serum Tryptase Test"],
            "explanation": "A rapid-onset allergic reaction involving airway swelling or difficulty breathing is anaphylaxis, a life-threatening medical emergency.",
            "supportive_advice": [
                "Administer epinephrine auto-injector (EpiPen) immediately if available.",
                "Lie flat with legs elevated if possible.",
                "Seek emergency medical services right away."
            ]
        },
        "Appendicitis": {
            "symptoms": ["abdominal pain", "right lower quadrant pain", "loss of appetite", "nausea", "vomiting", "fever"],
            "risk_factors": ["age"],
            "base_severity": 8,
            "care_level": "emergency",
            "recommended_tests": ["Complete Blood Count (CBC)", "Abdominal Ultrasound", "CT Scan of the Abdomen"],
            "explanation": "Abdominal pain migrating to the right lower quadrant, loss of appetite, and nausea are key symptoms of appendicitis.",
            "supportive_advice": [
                "Do not eat or drink anything (keep stomach empty for potential surgery).",
                "Do not apply heat or take laxatives/painkillers.",
                "Go to the nearest emergency department."
            ]
        },
        "Dengue": {
            "symptoms": ["high fever", "pain behind eyes", "rash", "joint pain", "body aches", "muscle pain"],
            "risk_factors": ["recent travel", "tropical climate"],
            "base_severity": 7,
            "care_level": "urgent",
            "recommended_tests": ["Complete Blood Count (CBC)", "Dengue NS1 Antigen Test", "Dengue IgM/IgG Antibody Test"],
            "explanation": "High fever, joint/muscle pain ('breakbone fever'), skin rash, and retro-orbital pain match the classic clinical presentation of Dengue.",
            "supportive_advice": [
                "Stay well-hydrated with water and oral rehydration solutions.",
                "Take paracetamol for fever control.",
                "Avoid NSAIDs like ibuprofen, naproxen, or aspirin due to bleeding risk.",
                "Seek immediate care if warning signs (severe abdominal pain, bleeding) develop."
            ]
        },
        "Pneumonia": {
            "symptoms": ["cough", "fever", "shortness of breath", "chest pain", "coughing up mucus", "chills"],
            "risk_factors": ["age", "smoking", "asthma", "chronic lung disease", "immunocompromised"],
            "base_severity": 7,
            "care_level": "urgent",
            "recommended_tests": ["Chest X-ray", "Complete Blood Count (CBC)", "Sputum Culture", "Pulse Oximetry"],
            "explanation": "Fever, cough with yellow/green phlegm, shortness of breath, and chest pain during deep breathing suggest pneumonia.",
            "supportive_advice": [
                "Get adequate rest and stay hydrated.",
                "Monitor your oxygen saturation and temperature regularly.",
                "Consult a doctor for appropriate antibiotics or antiviral prescription.",
                "Seek emergency care if you experience severe shortness of breath."
            ]
        },
        "Urinary Tract Infection": {
            "symptoms": ["burning urination", "cloudy urine", "frequent urination", "lower abdominal pain", "strong-smelling urine"],
            "risk_factors": ["pregnancy", "diabetes", "female"],
            "base_severity": 4,
            "care_level": "clinic",
            "recommended_tests": ["Urinalysis", "Urine Culture"],
            "explanation": "Pain/burning during urination, frequent urge, cloudy or strong-smelling urine suggest a urinary tract infection.",
            "supportive_advice": [
                "Drink plenty of water to help flush out the urinary tract.",
                "Avoid caffeine, alcohol, and spicy foods which can irritate the bladder.",
                "Schedule a clinic appointment for urinalysis and possible antibiotics."
            ]
        },
        "Kidney Stones": {
            "symptoms": ["severe back pain", "flank pain", "pain radiating to groin", "blood in urine", "nausea", "vomiting"],
            "risk_factors": ["dehydration", "family history", "dietary factors"],
            "base_severity": 6,
            "care_level": "urgent",
            "recommended_tests": ["CT Scan of the Abdomen/Pelvis (Non-contrast)", "Urinalysis", "Renal Ultrasound"],
            "explanation": "Severe, sharp flank pain radiating to the lower abdomen/groin, often accompanied by blood in the urine, is highly typical of kidney stones.",
            "supportive_advice": [
                "Drink water if tolerated to help pass the stone.",
                "Manage pain with approved over-the-counter pain relievers.",
                "Seek urgent care if pain is unmanageable or if you develop a fever or severe vomiting."
            ]
        },
        "Migraine": {
            "symptoms": ["headache", "severe headache", "nausea", "sensitivity to light", "sensitivity to sound", "visual aura"],
            "risk_factors": ["family history", "stress", "female"],
            "base_severity": 4,
            "care_level": "clinic",
            "recommended_tests": ["Neurological Examination", "Brain MRI (if symptoms are atypical or new)"],
            "explanation": "A severe, throbbing headache, often unilateral, accompanied by nausea and sensitivity to light or sound matches a migraine.",
            "supportive_advice": [
                "Rest in a dark, quiet, cool room.",
                "Apply a cold compress to your forehead or temples.",
                "Keep a headache diary to identify trigger factors.",
                "Avoid caffeine and known trigger foods."
            ]
        },
        "Diabetes": {
            "symptoms": ["frequent urination", "excessive thirst", "increased appetite", "unexplained weight loss", "fatigue", "blurry vision"],
            "risk_factors": ["family history", "obesity", "sedentary lifestyle", "age"],
            "base_severity": 3,
            "care_level": "clinic",
            "recommended_tests": ["Fasting Blood Sugar Test", "HbA1c Test", "Oral Glucose Tolerance Test"],
            "explanation": "Excessive thirst, frequent urination, fatigue, and blurry vision can indicate hyperglycemia or underlying diabetes mellitus.",
            "supportive_advice": [
                "Avoid sugar-sweetened beverages and high-glycemic foods.",
                "Establish a regular exercise routine.",
                "Schedule a checkup with a primary care doctor for blood glucose screening."
            ]
        },
        "Asthma Exacerbation": {
            "symptoms": ["wheezing", "shortness of breath", "cough", "chest tightness", "difficulty breathing"],
            "risk_factors": ["allergies", "smoking", "respiratory infection", "asthma"],
            "base_severity": 6,
            "care_level": "urgent",
            "recommended_tests": ["Spirometry", "Peak Expiratory Flow Rate", "Chest X-Ray"],
            "explanation": "Wheezing, shortness of breath, and chest tightness point towards an acute flare-up of asthma.",
            "supportive_advice": [
                "Use your rescue inhaler (albuterol) as prescribed.",
                "Remove yourself from potential triggers (smoke, dust, pollen).",
                "Sit upright and try to stay calm.",
                "Seek immediate emergency care if breathing does not improve."
            ]
        },
        "Common Cold": {
            "symptoms": ["cough", "runny nose", "sore throat", "sneezing", "mild headache", "congestion"],
            "risk_factors": [],
            "base_severity": 1,
            "care_level": "home",
            "recommended_tests": [],
            "explanation": "Mild upper respiratory symptoms such as runny nose, sneezing, scratchy throat, and mild cough are consistent with a viral common cold.",
            "supportive_advice": [
                "Get plenty of rest and sleep.",
                "Stay well-hydrated by drinking water, warm tea, or broths.",
                "Use saline nasal sprays to relieve congestion.",
                "Gargle with warm salt water for throat irritation."
            ]
        }
    }

    @classmethod
    def get_condition_details(cls, name: str) -> Dict[str, Any]:
        return cls.CONDITIONS.get(name, {})
