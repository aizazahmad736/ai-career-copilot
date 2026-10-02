from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, UniqueConstraint

from app.core.database import Base, utcnow


class LearningPlan(Base):
    __tablename__ = "learning_plans"
    __table_args__ = (UniqueConstraint("analysis_id", name="uq_learning_plan_analysis"),)

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("resume_analyses.id", ondelete="CASCADE"), nullable=False)
    duration_weeks = Column(Integer, nullable=False, default=6)
    milestones = Column(JSON, nullable=False, default=list)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)