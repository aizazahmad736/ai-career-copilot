from sqlalchemy import Column, DateTime, ForeignKey, Integer, JSON, UniqueConstraint

from app.core.database import Base, utcnow


class ResumeVersion(Base):
    __tablename__ = "resume_versions"
    __table_args__ = (UniqueConstraint("analysis_id", name="uq_resume_version_analysis"),)

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(Integer, ForeignKey("resume_analyses.id", ondelete="CASCADE"), nullable=False)
    version_number = Column(Integer, nullable=False)
    parsed_data = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=utcnow)