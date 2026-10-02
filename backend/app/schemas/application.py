from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field

ApplicationStatus = Literal["saved", "applied", "interviewing", "offer", "rejected"]


class ApplicationCreateRequest(BaseModel):
    job_key: str = Field(min_length=1, max_length=255)
    analysis_id: Optional[int] = None
    target_role: Optional[str] = Field(default=None, max_length=100)
    title: str = Field(min_length=1, max_length=255)
    company: str = Field(min_length=1, max_length=255)
    url: str = Field(min_length=1, max_length=2000)


class ApplicationStatusRequest(BaseModel):
    status: ApplicationStatus
    notes: Optional[str] = Field(default=None, max_length=4000)


class ApplicationResponse(BaseModel):
    id: int
    analysis_id: Optional[int] = None
    job_key: str
    target_role: Optional[str] = None
    title: str
    company: str
    url: str
    status: ApplicationStatus
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime