from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class InterviewCreateRequest(BaseModel):
    analysis_id: int
    mode: str = "mixed"
    question_count: int = Field(default=5, ge=3, le=8)
    custom_gemini_api_key: Optional[str] = None


class InterviewAnswerRequest(BaseModel):
    answer: str = Field(min_length=10, max_length=10000)
    custom_gemini_api_key: Optional[str] = None


class InterviewSessionResponse(BaseModel):
    id: int
    analysis_id: int
    target_role: str
    mode: str
    questions: List[Dict[str, str]]
    responses: List[Dict]
    total_score: Optional[float] = None
    status: str
    created_at: datetime
    completed_at: Optional[datetime] = None