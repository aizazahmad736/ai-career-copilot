from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from app.schemas.resume import ParsedResumeData

class SkillMatchItem(BaseModel):
    skill: str
    category: str = "General"  # Languages, Frameworks, Databases, Tools, Concepts, Soft Skills
    status: str  # "matched", "partial", "missing", "bonus"
    importance: str = "critical"  # "critical", "important", "bonus"
    evidence_or_tip: Optional[str] = None

class ATSFeedback(BaseModel):
    overall_ats_score: int = Field(default=75, ge=0, le=100)
    readability_score: int = Field(default=80, ge=0, le=100)
    impact_metrics_score: int = Field(default=65, ge=0, le=100)
    strengths: List[str] = []
    weaknesses: List[str] = []
    actionable_bullet_fixes: List[Dict[str, str]] = []  # e.g. [{"original": "Worked on APIs", "improved": "Architected and deployed 4 RESTful microservices using FastAPI, reducing response latency by 35%"}]

class ActionableRecommendation(BaseModel):
    priority: str = "High"  # "High", "Medium", "Low"
    title: str
    description: str
    target_skill: str
    estimated_time: str
    learning_path: List[str] = []

class SkillGapAnalysisRequest(BaseModel):
    target_role: str = "Junior Full Stack Developer"
    target_experience_level: str = "Entry-Level / Junior"
    job_description: Optional[str] = None
    custom_gemini_api_key: Optional[str] = None

class SkillGapAnalysisResponse(BaseModel):
    id: Optional[int] = None
    target_role: str
    experience_level: str
    match_score: float = Field(ge=0.0, le=100.0)
    candidate_name: Optional[str] = "Candidate"
    headline: Optional[str] = None
    summary: Optional[str] = None
    parsed_resume: ParsedResumeData
    matched_skills: List[SkillMatchItem] = []
    partial_skills: List[SkillMatchItem] = []
    missing_critical_skills: List[SkillMatchItem] = []
    bonus_skills: List[SkillMatchItem] = []
    ats_feedback: ATSFeedback
    recommendations: List[ActionableRecommendation] = []
    is_demo_mode: bool = False
