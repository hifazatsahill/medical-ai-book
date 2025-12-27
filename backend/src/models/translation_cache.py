from sqlalchemy import Column, String, Text, DateTime, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..database import Base


class TranslationCache(Base):
    __tablename__ = "translation_cache"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content_hash = Column(String, unique=True, nullable=False, index=True)  # Hash of original content
    original_content = Column(Text, nullable=False)
    translated_content = Column(Text, nullable=False)
    source_language = Column(String, default="en", nullable=False)
    target_language = Column(String, default="ur", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_accessed = Column(DateTime(timezone=True), nullable=True)