# pyrefly: ignore [missing-import]
from fastapi import APIRouter
from uuid import uuid4

router = APIRouter(
    prefix="/session",
    tags=["Session"]
)

sessions = {}


@router.post("/start")
def start_session():
    session_id = str(uuid4())
    sessions[session_id] = {
        "messages": [],
        "vitals": {},
        "voice": {}
    }
    return {"session_id": session_id}


@router.get("/{session_id}")
def get_session(session_id: str):
    return sessions.get(session_id, {})