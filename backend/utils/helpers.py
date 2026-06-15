import json
import re


def extract_json(raw):

    raw = raw.strip()

    match = re.search(r"\{.*\}", raw, re.DOTALL)

    if match:
        raw = match.group(0)

    try:
        return json.loads(raw)

    except:

        return {
            "message": raw,
            "extracted_symptoms": [],
            "body_regions": [],
            "severity_score": 0,
            "care_level": "HOME_CARE",
            "emergency_flag": False,
            "next_question": None,
            "triage_complete": False,
            "summary": ""
        }