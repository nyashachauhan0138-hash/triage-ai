# pyrefly: ignore [missing-import]
from fastapi import APIRouter

from models.chat import ChatRequest
from services.groq_service import GroqService
from utils.helpers import extract_json

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("")
@router.post("/")
async def chat(request: ChatRequest):

    raw = GroqService.generate(
        request.messages
    )

    data = extract_json(raw)

    # Run local custom-trained classifier on the latest user message
    from services.symptom_classifier_service import SymptomClassifierService
    last_message = request.messages[-1].content if request.messages else ""
    local_prediction = SymptomClassifierService.predict(last_message)
    data["local_severity_prediction"] = local_prediction

    severity_score = data.get("severity_score", 0)
    try:
        severity_score = float(severity_score) if severity_score is not None else 0
    except (ValueError, TypeError):
        severity_score = 0

    is_emergency = (
        severity_score >= 8 or 
        data.get("emergency_flag") is True or 
        str(data.get("care_level")).upper() == "EMERGENCY"
    )
    data["emergency_mode"] = is_emergency

    return data