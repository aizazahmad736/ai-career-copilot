from typing import List, Optional, Dict
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class PersonalInfo(BaseModel):
    name: Optional[str] = "Candidate"
    email: Optional[str] = None
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    portfolio: Optional[str] = None

class WorkExperience(BaseModel):
    role: str
    company: str
    duration: Optional[str] = None
    location: Optional[str] = None
    bullet_points: List[str] = []

class EducationItem(BaseModel):
    degree: str
    institution: str
    year: Optional[str] = None
    gpa: Optional[str] = None

class ProjectItem(BaseModel):
    name: str
    description: str
    tech_stack: List[str] = []
    link: Optional[str] = None

class CategorizedSkills(BaseModel):
    languages: List[str] = []
    frameworks: List[str] = []
    databases: List[str] = []
    tools_and_cloud: List[str] = []
    core_concepts: List[str] = []
    soft_skills: List[str] = []

class ParsedResumeData(BaseModel):
    personal_info: PersonalInfo = Field(default_factory=PersonalInfo)
    professional_headline: Optional[str] = None
    executive_summary: Optional[str] = None
    skills: CategorizedSkills = Field(default_factory=CategorizedSkills)
    experience: List[WorkExperience] = []
    education: List[EducationItem] = []
    projects: List[ProjectItem] = []
    certifications: List[str] = []

class ResumeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: Optional[int] = None
    filename: str
    file_type: str
    file_size_bytes: Optional[int] = None
    created_at: Optional[datetime] = None
    parsed_data: Optional[ParsedResumeData] = None
