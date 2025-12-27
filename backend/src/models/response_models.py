from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from uuid import UUID


# Base response model
class BaseResponse(BaseModel):
    """Base response model with standard fields"""
    success: bool = True
    message: Optional[str] = None
    timestamp: datetime = datetime.now()


# User-related response models
class UserResponse(BaseModel):
    id: UUID
    email: str
    name: str
    is_active: bool = True
    created_at: datetime
    updated_at: Optional[datetime] = None


class UserProfileResponse(BaseModel):
    id: UUID
    user_id: UUID
    profession: Optional[str] = None
    experience_level: Optional[str] = None
    technical_background: Optional[str] = None
    preferences: Optional[Dict[str, Any]] = {}
    created_at: datetime
    updated_at: Optional[datetime] = None


class UserRegistrationResponse(BaseResponse):
    user: UserResponse
    access_token: Optional[str] = None
    token_type: Optional[str] = None


class UserProfileUpdateResponse(BaseResponse):
    profile: Optional[UserProfileResponse] = None


# Chapter-related response models
class ChapterResponse(BaseModel):
    id: UUID
    title: str
    slug: str
    content: Optional[str] = None  # Omit for list views
    content_urdu: Optional[str] = None
    chapter_number: int
    word_count: Optional[int] = None
    reading_time: Optional[int] = None
    chapter_metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None


class ChapterListResponse(BaseResponse):
    chapters: List[ChapterResponse]
    total: int


# Progress-related response models
class UserProgressResponse(BaseModel):
    id: UUID
    user_id: UUID
    chapter_id: UUID
    progress_percentage: int
    time_spent: Optional[int] = None
    notes: Optional[str] = None
    bookmarks: Optional[List[str]] = []
    last_accessed: Optional[datetime] = None
    completed: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None


class UserProgressUpdateResponse(BaseResponse):
    progress: UserProgressResponse


# Chat-related response models
class ChatSessionResponse(BaseModel):
    id: UUID
    user_id: Optional[UUID] = None
    session_token: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None


class ChatMessageResponse(BaseModel):
    id: UUID
    session_id: UUID
    role: str  # "user" or "assistant"
    content: str
    context_type: Optional[str] = None
    selected_text: Optional[str] = None
    timestamp: datetime
    sources: Optional[List[Dict[str, Any]]] = []


class ChatQueryResponse(BaseResponse):
    response: str
    sources: List[Dict[str, Any]]
    confidence: float


# Translation-related response models
class TranslationResponse(BaseResponse):
    original_content: str
    translated_content: str
    source_language: str = "en"
    target_language: str = "ur"


# Personalization-related response models
class PersonalizationResponse(BaseResponse):
    original_content: str
    personalized_content: str
    adaptation_notes: List[str]