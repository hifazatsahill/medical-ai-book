from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime
from uuid import UUID


class EmbedConfigurationBase(BaseModel):
    book_id: UUID
    embed_type: str  # 'js_widget' or 'iframe'
    configuration: Optional[Dict[str, Any]] = {}


class EmbedConfigurationCreate(EmbedConfigurationBase):
    pass


class EmbedConfigurationUpdate(BaseModel):
    configuration: Optional[Dict[str, Any]] = None


class EmbedConfiguration(EmbedConfigurationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True