from typing import List

class EmergencyDetector:
    # Key clinical symptoms that represent immediate medical emergencies
    EMERGENCY_RED_FLAGS = [
        "crushing chest pain",
        "loss of consciousness",
        "severe breathing difficulty",
        "stroke symptoms",
        "heavy bleeding",
        "seizure",
        "coughing up blood",
        "severe allergic reaction",
        "blue lips",
        "severe burns",
        "major trauma",
        "facial droop",
        "sudden numbness",
        "slurred speech",
        "anaphylaxis"
    ]

    @classmethod
    def check_emergency(cls, symptoms: List[str], text: str = "") -> bool:
        """
        Scans both the extracted symptoms list and the raw text for emergency conditions.
        """
        text_lower = text.lower()
        
        # Check standard list
        for s in symptoms:
            s_lower = s.lower()
            if s_lower in cls.EMERGENCY_RED_FLAGS:
                return True
            # Substring safety checks
            if "crushing chest" in s_lower:
                return True
            if "unconscious" in s_lower or "passed out" in s_lower:
                return True
            if "stroke" in s_lower:
                return True
            if "heavy bleeding" in s_lower or "bleeding heavily" in s_lower:
                return True
            if "seizure" in s_lower or "convulsion" in s_lower:
                return True
            if "coughing blood" in s_lower or "coughing up blood" in s_lower:
                return True
            if "anaphylaxis" in s_lower or "severe allergic" in s_lower:
                return True
            if "blue lips" in s_lower or "lips turned blue" in s_lower:
                return True
            if "severe burn" in s_lower:
                return True
            if "major trauma" in s_lower:
                return True

        # Check raw text for safety fallback
        raw_checks = [
            "crushing chest pain",
            "cannot catch my breath",
            "can't catch my breath",
            "passed out",
            "lost consciousness",
            "slurred speech",
            "coughing up blood",
            "lips turned blue",
            "heavy bleeding",
            "sudden numbness",
            "anaphylaxis"
        ]
        if any(chk in text_lower for chk in raw_checks):
            return True

        return False
