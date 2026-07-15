# pyrefly: ignore [missing-import]
from fastapi import FastAPI
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
from pathlib import Path

# Load env file using absolute path relative to this file
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

from routers.chat import router as chat_router
from routers.session import router as session_router
from routers.vitals import router as vitals_router
from routers.voice import router as voice_router
from routers.report import router as report_router

app = FastAPI(
    title="TriageAI API",
    description="Multimodal medical triage backend API",
    version="1.0.0"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register all modular routers
app.include_router(chat_router)
app.include_router(session_router)
app.include_router(vitals_router)
app.include_router(voice_router)
app.include_router(report_router)


@app.get("/")
def root():
    return {"status": "TriageAI backend running"}