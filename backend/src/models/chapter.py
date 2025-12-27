from sqlalchemy import Column, String, Text, DateTime, Integer, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..database import Base


class BookChapter(Base):
    __tablename__ = "book_chapters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False, index=True)  # URL-friendly
    content = Column(Text, nullable=False)  # Markdown format
    content_urdu = Column(Text, nullable=True)  # Translated content in Urdu
    chapter_number = Column(Integer, nullable=False)
    word_count = Column(Integer, nullable=True)  # Auto-calculated
    reading_time = Column(Integer, nullable=True)  # Estimated minutes, Auto-calculated
    chapter_metadata = Column(JSON, nullable=True)  # Additional chapter metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())