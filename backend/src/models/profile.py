from sqlalchemy import Column, String, DateTime, JSON, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    profession = Column(String, nullable=True)  # e.g., "pathologist", "lab technician", "student", "software engineer"
    experience_level = Column(String, nullable=True)  # e.g., "beginner", "intermediate", "advanced"
    technical_background = Column(String, nullable=True)  # e.g., "medical", "software", "mixed"
    preferences = Column(JSON, nullable=True)  # Personalization settings
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())