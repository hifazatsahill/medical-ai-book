from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
from uuid import UUID
import uuid


class SessionDataBase(BaseModel):
    book_id: UUID
    session_token: str
    metadata: Optional[Dict[str, Any]] = {}
    conversation_history: Optional[List[Dict[str, Any]]] = []


class SessionDataCreate(SessionDataBase):
    pass


class SessionDataUpdate(BaseModel):
    metadata: Optional[Dict[str, Any]] = None
    conversation_history: Optional[List[Dict[str, Any]]] = None


class SessionData(SessionDataBase):
    id: UUID
    created_at: datetime
    last_accessed: datetime
    expires_at: datetime

    class Config:
        from_attributes = True