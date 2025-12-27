"""Database models and base configuration."""
from sqlalchemy.ext.declarative import declarative_base
from .database.connection import Base, engine, close_db_connection

# Import all models to ensure they are registered with SQLAlchemy
from .models.user import User
from .models.profile import UserProfile
from .models.chapter import BookChapter
from .models.progress import UserProgress
from .models.chat import ChatSession, ChatMessage
from .models.translation_cache import TranslationCache

__all__ = [
    "Base",
    "engine",
    "close_db_connection",
    "User",
    "UserProfile",
    "BookChapter",
    "UserProgress",
    "ChatSession",
    "ChatMessage",
    "TranslationCache"
]