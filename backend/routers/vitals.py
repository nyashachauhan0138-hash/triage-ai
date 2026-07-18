# pyrefly: ignore [missing-import]
from fastapi import APIRouter, UploadFile, File
import os

from services.rppg_service import RPPGService

router = APIRouter(
    prefix="/vitals",
    tags=["Vitals"]
)


@router.post("/analyze")
async def analyze_vitals(
    file: UploadFile = File(...)
):

    import uuid
    unique_id = str(uuid.uuid4())
    # Keep the original extension if present
    ext = os.path.splitext(file.filename)[1] if file.filename else ".mp4"
    temp_path = f"temp_vitals_{unique_id}{ext}"

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        result = RPPGService.analyze(temp_path)
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return result