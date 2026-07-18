# pyrefly: ignore [missing-import]
from fastapi import APIRouter, BackgroundTasks, UploadFile, File
# pyrefly: ignore [missing-import]
from fastapi.responses import FileResponse
import os
import uuid

# pyrefly: ignore [missing-import]
from services.report_service import ReportService
from services.report_analysis_service import ReportAnalysisService

router = APIRouter(
    prefix="/report",
    tags=["Report"]
)


def cleanup_file(path: str):
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception as e:
        print(f"Error cleaning up file {path}: {e}")


@router.post("/generate")
def generate_report(payload: dict, background_tasks: BackgroundTasks):

    path = ReportService.generate(payload)

    background_tasks.add_task(cleanup_file, path)

    return FileResponse(
        path,
        media_type="application/pdf",
        filename="triage_report.pdf"
    )


@router.post("/analyze")
async def analyze_report(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...)
):
    unique_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1] if file.filename else ".pdf"
    temp_path = f"temp_report_{unique_id}{ext}"

    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        result = ReportAnalysisService.analyze_report(temp_path)
    finally:
        background_tasks.add_task(cleanup_file, temp_path)

    return result