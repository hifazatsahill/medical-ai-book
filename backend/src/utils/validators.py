from pydantic import BaseModel, validator, ValidationError
from typing import Optional, List
import uuid
import re


class BookContentValidator(BaseModel):
    title: str
    author: str
    content: str
    metadata: Optional[dict] = {}

    @validator('title')
    def validate_title(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Title is required')
        if len(v) > 500:
            raise ValueError('Title must be less than 500 characters')
        return v.strip()

    @validator('author')
    def validate_author(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Author is required')
        if len(v) > 200:
            raise ValueError('Author name must be less than 200 characters')
        return v.strip()

    @validator('content')
    def validate_content(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Content is required')
        if len(v) < 100:  # Minimum content length
            raise ValueError('Content is too short to be meaningful')
        return v

    @validator('metadata')
    def validate_metadata(cls, v):
        if v is None:
            return {}
        # Ensure metadata is a dict and doesn't contain sensitive keys
        if not isinstance(v, dict):
            raise ValueError('Metadata must be a dictionary')
        return v


class QueryValidator(BaseModel):
    query: str
    sessionId: str
    selectedText: Optional[str] = None

    @validator('query')
    def validate_query(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Query is required')
        if len(v) > 1000:  # Limit query length
            raise ValueError('Query is too long')
        return v.strip()

    @validator('sessionId')
    def validate_session_id(cls, v):
        try:
            uuid.UUID(v)
        except ValueError:
            raise ValueError('Session ID must be a valid UUID')
        return v

    @validator('selectedText')
    def validate_selected_text(cls, v):
        if v is not None and len(v.strip()) == 0:
            raise ValueError('Selected text cannot be empty if provided')
        if v is not None and len(v) > 10000:  # Limit selected text length
            raise ValueError('Selected text is too long')
        return v


class SessionValidator(BaseModel):
    bookId: str
    metadata: Optional[dict] = {}

    @validator('bookId')
    def validate_book_id(cls, v):
        try:
            uuid.UUID(v)
        except ValueError:
            raise ValueError('Book ID must be a valid UUID')
        return v

    @validator('metadata')
    def validate_session_metadata(cls, v):
        if v is None:
            return {}
        if not isinstance(v, dict):
            raise ValueError('Metadata must be a dictionary')
        return v


def validate_uuid(uuid_string: str) -> bool:
    """
    Validate if a string is a valid UUID
    """
    try:
        uuid.UUID(uuid_string)
        return True
    except ValueError:
        return False


def validate_email(email: str) -> bool:
    """
    Basic email validation
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None