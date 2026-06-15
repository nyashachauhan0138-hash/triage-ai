from typing import Dict


class TriageEngine:

    @staticmethod
    def symptom_score(symptoms):

        score = 0

        critical = [
            "chest pain",
            "can't breathe",
            "stroke",
            "unconscious",
            "seizure",
            "blood vomiting",
            "heart attack"
        ]

        high = [
            "fever",
            "dizziness",
            "vomiting",
            "shortness of breath",
            "rapid heartbeat"
        ]

        moderate = [
            "headache",
            "fatigue",
            "cough",
            "body pain"
        ]

        for symptom in symptoms:

            s = symptom.lower()

            if any(word in s for word in critical):
                score += 4

            elif any(word in s for word in high):
                score += 2

            elif any(word in s for word in moderate):
                score += 1

        return min(score, 10)

    @staticmethod
    def vitals_score(heart_rate=None, spo2=None):

        score = 0

        if heart_rate:

            if heart_rate > 130:
                score += 4

            elif heart_rate > 110:
                score += 2

        if spo2:

            if spo2 < 90:
                score += 4

            elif spo2 < 95:
                score += 2

        return min(score, 10)

    @staticmethod
    def voice_score(stress_score=None):

        if stress_score is None:
            return 0

        if stress_score > 85:
            return 4

        if stress_score > 65:
            return 2

        return 1

    @staticmethod
    def fusion_engine(
        symptoms=[],
        heart_rate=None,
        spo2=None,
        stress_score=None
    ) -> Dict:

        symptom_score = TriageEngine.symptom_score(
            symptoms
        )

        vitals_score = TriageEngine.vitals_score(
            heart_rate,
            spo2
        )

        voice_score = TriageEngine.voice_score(
            stress_score
        )

        final_score = (
            symptom_score * 0.5 +
            vitals_score * 0.3 +
            voice_score * 0.2
        )

        final_score = round(final_score, 1)

        severity = "LOW"
        care_level = "HOME_CARE"
        emergency_flag = False

        if final_score >= 8:
            severity = "CRITICAL"
            care_level = "EMERGENCY"
            emergency_flag = True

        elif final_score >= 6:
            severity = "HIGH"
            care_level = "HOSPITAL"

        elif final_score >= 3:
            severity = "MODERATE"
            care_level = "CLINIC"

        recommendation = TriageEngine.recommendation(
            severity
        )

        return {
            "severity": severity,
            "severity_score": final_score,
            "care_level": care_level,
            "emergency_flag": emergency_flag,
            "recommendation": recommendation
        }

    @staticmethod
    def recommendation(severity):

        recommendations = {
            "LOW": "Monitor symptoms and rest.",
            "MODERATE": "Consult a nearby clinic.",
            "HIGH": "Visit a hospital immediately.",
            "CRITICAL": "Call emergency services now."
        }

        return recommendations.get(
            severity,
            "Monitor condition."
        )