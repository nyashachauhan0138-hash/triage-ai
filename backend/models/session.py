from fastapi import APIRouter
from uuid import uuid4
from pydantic import BaseModel
from typing import Dict, Any

router = APIRouter(
    prefix="/session",
    tags=["Session"]
)

sessions = {}


class Session(BaseModel):
    session_id: str
    data: Dict[str, Any]


@router.post("/start")
def start_session():

    session_id = str(uuid4())

    sessions[session_id] = {
        "messages": [],
        "vitals": {},
        "voice": {}
    }

    return {
        "session_id": session_id
    }


@router.get("/{session_id}")
def get_session(session_id: str):

    return sessions.get(session_id, {})