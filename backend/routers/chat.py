# pyrefly: ignore [missing-import]
from fastapi import APIRouter

from models.chat import ChatRequest
from services.triage import TriageCoordinator
from services.symptom_classifier_service import SymptomClassifierService

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


@router.post("")
@router.post("/")
async def chat(request: ChatRequest):

    # 1. Run local custom-trained classifier on the latest user message
    last_message = request.messages[-1].content if request.messages else ""
    local_prediction = SymptomClassifierService.predict(last_message)

    # 2. Run the main TriageCoordinator pipeline
    data = TriageCoordinator.triage(request.messages)
    
    # 3. Augment with local prediction and emergency mode
    data["local_severity_prediction"] = local_prediction
    data["emergency_mode"] = data["emergency_flag"]

    return data