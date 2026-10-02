from sqlalchemy import Column, Integer, String, Text, DateTime
from app.core.database import Base, utcnow

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50), nullable=False)
    file_size_bytes = Column(Integer, nullable=True)
    raw_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=utcnow)
