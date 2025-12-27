from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # API Configuration
    app_name: str = "Integrated RAG Chatbot API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Cohere Configuration
    cohere_api_key: str
    
    # Qdrant Configuration
    qdrant_url: str
    qdrant_api_key: Optional[str] = None
    
    # Database Configuration
    database_url: str
    
    # Rate Limiting
    queries_per_minute: int = 10
    
    # Text Processing
    min_chunk_size: int = 512
    max_chunk_size: int = 1024
    
    class Config:
        env_file = ".env"


settings = Settings()