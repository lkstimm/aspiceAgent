"""
Configuration management for the ASPICE Agent platform
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    database_url: str = "postgresql://user:password@localhost:5432/aspice_agent"
    
    # Anthropic Claude API
    anthropic_api_key: str = ""
    
    # Redis (for Celery)
    redis_url: str = "redis://localhost:6379/0"
    
    # JWT
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # Application
    debug: bool = True
    environment: str = "development"
    
    # ChromaDB
    chroma_persist_directory: str = "./chroma_db"
    
    # File uploads
    max_file_size: int = 52428800  # 50MB in bytes
    upload_directory: str = "./uploads"
    
    # CORS
    allowed_origins: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
_settings: Optional[Settings] = None


def get_settings() -> Settings:
    """Get application settings (singleton)"""
    global _settings
    if _settings is None:
        _settings = Settings()
    return _settings