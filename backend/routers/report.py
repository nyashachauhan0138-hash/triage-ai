# pyrefly: ignore [missing-import]
from fastapi import APIRouter, BackgroundTasks
# pyrefly: ignore [missing-import]
from fastapi.responses import FileResponse
import os

# pyrefly: ignore [missing-import]
from services.report_service import ReportService

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