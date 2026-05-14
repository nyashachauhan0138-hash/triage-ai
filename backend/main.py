from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
from google import genai
from google.genai import types
import json
import os

load_dotenv()

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are TriageAI, an empathetic AI-powered medical triage assistant helping patients in underserved areas.

Ask ONE focused question at a time. Be warm, clear, and simple.

CRITICAL: Every single response MUST be valid JSON only. No text before or after. No markdown. No code blocks. No ```json fences.

Return exactly this structure:
{
  "message": "Your conversational response to the patient",
  "extracted_symptoms": ["symptom1", "symptom2"],
  "body_regions": ["chest", "head"],
  "severity_score": 5.0,
  "care_level": "HOME_CARE",
  "emergency_flag": false,
  "next_question": "Your next question or null if triage complete",
  "triage_complete": false,
  "summary": "Clinical summary only when triage_complete is true, else empty string"
}

body_regions ONLY from: head, neck, chest, abdomen, back, left_arm, right_arm, left_leg, right_leg, pelvis
care_level ONLY: HOME_CARE, CLINIC, EMERGENCY

Rules:
- chest pain + shortness of breath: emergency_flag = true, care_level = EMERGENCY immediately
- fever + headache + stiff neck: emergency_flag = true, care_level = EMERGENCY
- After 5-6 exchanges set triage_complete = true and write summary
- severity_score: 1-3 minor, 4-6 moderate, 7-10 severe
- NEVER diagnose. Always preliminary guidance only."""

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]

@app.get("/")
def root():
    return {"status": "TriageAI backend running"}

@app.post("/chat")
async def chat(request: ChatRequest):
    history = []
    for m in request.messages[:-1]:
        role = "user" if m.role == "user" else "model"
        history.append(types.Content(role=role, parts=[types.Part(text=m.content)]))

    last_message = request.messages[-1].content

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.3,
        ),
        contents=history + [types.Content(role="user", parts=[types.Part(text=last_message)])]
    )

    raw = response.text.strip()

    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    try:
        data = json.loads(raw)
    except:
        data = {
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

    return data