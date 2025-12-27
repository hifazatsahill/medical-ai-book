from sqlalchemy import Column, String, Text, DateTime, JSON, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
from ..database import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)  # Optional for anonymous sessions
    session_token = Column(String, nullable=True)  # For anonymous users
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), server_default=func.now())
    is_active = Column(Boolean, default=True, nullable=False)


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("chat_sessions.id"), nullable=False)
    role = Column(String, nullable=False)  # Either "user" or "assistant"
    content = Column(Text, nullable=False)
    context_type = Column(String, nullable=True)  # Either "full_book" or "selected_text"
    selected_text = Column(Text, nullable=True)  # If context_type is "selected_text"
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    sources = Column(JSON, nullable=True)  # List of source references for RAG responses