from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint

from app.core.database import Base, utcnow


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (UniqueConstraint("user_id", "job_key", name="uq_application_user_job"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True, index=True)
    analysis_id = Column(Integer, ForeignKey("resume_analyses.id", ondelete="SET NULL"), nullable=True)
    job_key = Column(String(255), nullable=False)
    target_role = Column(String(100), nullable=True)
    title = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    url = Column(Text, nullable=False)
    status = Column(String(30), nullable=False, default="saved")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=utcnow)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow)