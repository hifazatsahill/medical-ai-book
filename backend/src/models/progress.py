from sqlalchemy import Column, String, Text, DateTime, Integer, Boolean, JSON, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..database import Base


class UserProgress(Base):
    __tablename__ = "user_progress"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("book_chapters.id"), nullable=False)
    progress_percentage = Column(Integer, nullable=False, default=0)  # 0-100
    time_spent = Column(Integer, nullable=True)  # Seconds
    notes = Column(Text, nullable=True)  # Optional user notes
    bookmarks = Column(JSON, nullable=True)  # List of bookmarked positions
    last_accessed = Column(DateTime(timezone=True), nullable=True)
    completed = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())