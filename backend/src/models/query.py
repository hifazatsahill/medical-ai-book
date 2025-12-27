from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserQueryBase(BaseModel):
    session_id: UUID
    query_text: str
    query_type: str  # 'full_book' or 'selected_text'
    selected_text: Optional[str] = None


class UserQueryCreate(UserQueryBase):
    pass


class UserQueryUpdate(BaseModel):
    selected_text: Optional[str] = None


class UserQuery(UserQueryBase):
    id: UUID
    timestamp: datetime

    class Config:
        from_attributes = True


class RetrievedSegmentBase(BaseModel):
    query_id: UUID
    chunk_id: UUID
    relevance_score: float
    content: str
    metadata: Optional[dict] = {}


class RetrievedSegmentCreate(RetrievedSegmentBase):
    pass


class RetrievedSegmentUpdate(BaseModel):
    relevance_score: Optional[float] = None


class RetrievedSegment(RetrievedSegmentBase):
    id: UUID
    retrieved_at: datetime

    class Config:
        from_attributes = True


class QueryResponse(BaseModel):
    response: str
    sources: Optional[list] = []
    session_id: str