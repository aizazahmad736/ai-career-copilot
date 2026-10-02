from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, JSON
from app.core.database import Base

class JobSearch(Base):
    __tablename__ = "job_searches"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("resume_analyses.id", ondelete="SET NULL"), nullable=True)
    target_role = Column(String(100), nullable=False)
    experience_level = Column(String(50), default="Entry-Level / Junior")
    query = Column(String(255), nullable=False)
    location = Column(String(150), nullable=True)
    remote_only = Column(Boolean, default=False)

    result_count = Column(Integer, default=0)
    top_match_score = Column(Float, default=0.0)
    sources_used = Column(JSON, default=list)
    results = Column(JSON, default=list)
    is_demo_mode = Column(Boolean, default=False)

    created_at = Column(DateTime, default=datetime.utcnow)
