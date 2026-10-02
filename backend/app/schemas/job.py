from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class JobSearchRequest(BaseModel):
    skills: Dict[str, List[str]] = {}  # Same categorized shape as CategorizedSkills from the CV analysis
    target_role: str = "Junior Full Stack Developer"
    experience_level: str = "Entry-Level / Junior"
    location: Optional[str] = None
    remote_only: bool = False
    limit: int = Field(default=20, ge=1, le=50)
    analysis_id: Optional[int] = None
    tavily_api_key: Optional[str] = None
    serper_api_key: Optional[str] = None

class JobMatch(BaseModel):
    id: str
    title: str
    company: str
    location: Optional[str] = None
    remote: bool = False
    url: str
    source: str  # "Remotive", "Arbeitnow", "Tavily", "Serper", "Sample"
    posted_at: Optional[str] = None
    job_type: Optional[str] = None
    salary: Optional[str] = None
    description_snippet: Optional[str] = None
    match_score: float = Field(ge=0.0, le=100.0)
    fit_label: str  # "Strong Match", "Good Match", "Stretch", "Low Match"
    fit_summary: str
    matched_skills: List[str] = []
    missing_skills: List[str] = []

class JobSearchResponse(BaseModel):
    id: Optional[int] = None
    target_role: str
    experience_level: str
    query: str
    total_found: int = 0
    sources_used: List[str] = []
    source_errors: Dict[str, str] = {}
    is_demo_mode: bool = False
    jobs: List[JobMatch] = []
