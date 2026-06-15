from pydantic import BaseModel
from typing import Optional, List


class VitalSigns(BaseModel):

    heart_rate: Optional[int] = None
    spo2: Optional[int] = None
    respiratory_rate: Optional[int] = None


class VoiceAnalysis(BaseModel):

    stress_score: int
    emotion: str
    pitch: Optional[float] = None


class SymptomAnalysis(BaseModel):

    extracted_symptoms: List[str]
    body_regions: List[str]


class TriageResult(BaseModel):

    severity: str
    severity_score: float
    care_level: str
    emergency_flag: bool
    recommendation: str


class MultimodalAssessment(BaseModel):

    symptoms: SymptomAnalysis
    vitals: VitalSigns
    voice: VoiceAnalysis
    triage: TriageResult