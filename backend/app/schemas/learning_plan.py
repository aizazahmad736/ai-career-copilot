from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class LearningMilestone(BaseModel):
    week: int
    focus: str
    skills: List[str]
    goal: str
    tasks: List[str]
    project_checkpoint: str
    estimated_hours: int = Field(ge=1, le=40)
    resources: List[dict[str, str]] = []
    completed: bool = False


class LearningPlanRequest(BaseModel):
    analysis_id: int
    duration_weeks: int = Field(default=6, ge=4, le=12)


class LearningPlanResponse(BaseModel):
    id: int
    analysis_id: int
    duration_weeks: int
    milestones: List[LearningMilestone]
    created_at: datetime
    updated_at: datetime


class MilestoneProgressRequest(BaseModel):
    completed: bool