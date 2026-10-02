from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, JSON, String

from app.core.database import Base, utcnow


class InterviewSession(Base):
    __tablename__ = "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("resume_analyses.id", ondelete="CASCADE"), nullable=False)
    target_role = Column(String(100), nullable=False)
    mode = Column(String(30), nullable=False, default="mixed")
    questions = Column(JSON, nullable=False, default=list)
    responses = Column(JSON, nullable=False, default=list)
    total_score = Column(Float, nullable=True)
    status = Column(String(20), nullable=False, default="in_progress")
    created_at = Column(DateTime, default=utcnow)
    completed_at = Column(DateTime, nullable=True)