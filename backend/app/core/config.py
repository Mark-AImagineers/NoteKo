"""
Application configuration settings.
"""
from typing import List
from pydantic_settings import BaseSettings
from app.core.metadata import metadata

class Settings(BaseSettings):
    """Application settings."""
    
    # Project Info
    PROJECT_NAME: str = metadata.name
    VERSION: str = metadata.version
    API_VERSION: str = metadata.api_version
    ENVIRONMENT: str = "development"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",  # React frontend
        "http://localhost:8000",  # FastAPI backend
    ]
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@db:5432/noteko"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Create global settings instance
settings = Settings()
