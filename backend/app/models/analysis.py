from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class ResumeAnalysis(Base):
    __tablename__ = "resume_analyses"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id", ondelete="CASCADE"), nullable=True)
    target_role = Column(String(100), nullable=False)
    experience_level = Column(String(50), default="Entry-Level / Junior")
    match_score = Column(Float, default=0.0)
    
    candidate_name = Column(String(150), nullable=True)
    candidate_email = Column(String(150), nullable=True)
    headline = Column(String(255), nullable=True)
    summary = Column(Text, nullable=True)
    
    extracted_skills = Column(JSON, default=dict)
    matched_skills = Column(JSON, default=list)
    partial_skills = Column(JSON, default=list)
    missing_skills = Column(JSON, default=list)
    bonus_skills = Column(JSON, default=list)
    recommendations = Column(JSON, default=list)
    ats_feedback = Column(JSON, default=dict)
    
    created_at = Column(DateTime, default=datetime.utcnow)
