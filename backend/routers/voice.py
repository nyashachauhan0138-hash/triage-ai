# pyrefly: ignore [missing-import]
from fastapi import APIRouter, UploadFile, File
import os

from services.voice_service import VoiceService

router = APIRouter(
    prefix="/voice",
    tags=["Voice"]
)


@router.post("/analyze")
async def analyze_voice(
    file: UploadFile = File(...)
):

    import uuid
    unique_id = str(uuid.uuid4())
    # Keep the original extension if present
    ext = os.path.splitext(file.filename)[1] if file.filename else ".wav"
    temp_path = f"temp_voice_{unique_id}{ext}"

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    result = VoiceService.analyze(temp_path)

    os.remove(temp_path)

    return result


from services.groq_service import GroqService

@router.post("/transcribe")
async def transcribe_voice(
    file: UploadFile = File(...)
):

    import uuid
    unique_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1] if file.filename else ".wav"
    temp_path = f"temp_transcribe_{unique_id}{ext}"

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    transcript = GroqService.transcribe(temp_path)

    os.remove(temp_path)

    return {"transcript": transcript}