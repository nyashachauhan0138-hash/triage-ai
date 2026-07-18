from typing import List, Dict, Any

class SeverityPredictor:

    @classmethod
    def predict_severity(
        cls, 
        symptoms: List[str], 
        emergency_flag: bool,
        vitals: Dict[str, Any] = None,
        voice: Dict[str, Any] = None,
        risk_factors: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Calculates severity score (0-10) and assigns label ('low', 'mild', 'moderate', 'high').
        """
        if emergency_flag:
            return {
                "severity_score": 10.0,
                "severity": "high"
            }
            
        score = 0.0
        
        # 1. Base Score from Symptoms
        critical = [
            "chest pain", "shortness of breath", "sudden numbness", "slurred speech",
            "loss of consciousness", "heavy bleeding", "seizure", "coughing up blood",
            "severe allergic reaction", "blue lips", "severe burns", "major trauma",
            "difficulty breathing"
        ]
        high = [
            "high fever", "severe headache", "stiff neck", "vomiting", "wheezing",
            "severe back pain", "blood in urine", "abdominal pain", "right lower quadrant pain",
            "difficulty swallowing"
        ]
        moderate = [
            "fever", "nausea", "cough", "coughing up mucus", "joint pain", "body aches",
            "muscle pain", "pain behind eyes", "burning urination", "cloudy urine",
            "frequent urination", "diarrhea", "excessive thirst", "blurry vision"
        ]
        
        has_critical = any(s in symptoms for s in critical)
        has_high = any(s in symptoms for s in high)
        has_mod = any(s in symptoms for s in moderate)
        
        if has_critical:
            score += 7.0
        elif has_high:
            score += 5.0
        elif has_mod:
            score += 3.0
        else:
            score += 1.0 # Low base for minor symptoms (cold, runny nose)
            
        # Add incremental score for multiple symptoms
        score += min(len(symptoms) * 0.4, 2.0)
        
        # 2. Vitals Adjustment
        if vitals:
            heart_rate = vitals.get("heart_rate")
            spo2 = vitals.get("spo2")
            if heart_rate:
                try:
                    hr_val = float(heart_rate)
                    if hr_val > 130:
                        score += 2.0
                    elif hr_val > 110:
                        score += 1.0
                except (ValueError, TypeError):
                    pass
            if spo2:
                try:
                    spo2_val = float(spo2)
                    if spo2_val < 90:
                        score = max(score, 9.0) # Dangerous hypoxia
                    elif spo2_val < 95:
                        score += 1.5
                except (ValueError, TypeError):
                    pass

        # 3. Voice Stress Adjustment
        if voice:
            stress_score = voice.get("stress_score")
            if stress_score:
                try:
                    stress_val = float(stress_score)
                    if stress_val > 80:
                        score += 1.0
                except (ValueError, TypeError):
                    pass

        # 4. Risk Factors Adjustment
        if risk_factors:
            age = risk_factors.get("age")
            try:
                if age and float(age) > 65:
                    score += 1.0
            except (ValueError, TypeError):
                pass
                
            high_risk_keys = ["pregnancy", "diabetes", "hypertension", "asthma", "chronic diseases", "smoking"]
            for key in high_risk_keys:
                val = risk_factors.get(key)
                if val is True or str(val).lower() in ["true", "yes", "1"]:
                    score += 0.5

        # Round and Cap
        final_score = round(min(max(score, 0.0), 10.0), 1)
        
        # Map to label
        # 0–2 → Low, 3–5 → Mild, 6–7 → Moderate, 8–10 → High
        if final_score >= 8.0:
            label = "high"
        elif final_score >= 6.0:
            label = "moderate"
        elif final_score >= 3.0:
            label = "mild"
        else:
            label = "low"
            
        return {
            "severity_score": final_score,
            "severity": label
        }
