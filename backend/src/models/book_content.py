from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID, uuid4
import uuid


class BookContentBase(BaseModel):
    title: str
    author: str
    content: str
    metadata: Optional[Dict[str, Any]] = {}


class BookContentCreate(BookContentBase):
    pass


class BookContentUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    content: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class BookContent(BookContentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    chunks: Optional[List['BookChunk']] = []

    class Config:
        from_attributes = True


class BookChunkBase(BaseModel):
    book_id: UUID
    content: str
    token_count: int
    chunk_index: int
    vector_id: str
    metadata: Optional[Dict[str, Any]] = {}


class BookChunkCreate(BookChunkBase):
    pass


class BookChunkUpdate(BaseModel):
    content: Optional[str] = None
    token_count: Optional[int] = None
    chunk_index: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None


class BookChunk(BookChunkBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# Forward reference for BookContent
BookContent.update_forward_refs()