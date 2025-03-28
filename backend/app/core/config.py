"""
Application configuration settings.
"""
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings.
    """
    # Application
    PROJECT_NAME: str = "NoteKo"
    VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    
    # Authentication
    SECRET_KEY: str = "your-secret-key-here"  # Change in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: Optional[str] = None
    TEST_DATABASE_URL: str = "sqlite+aiosqlite:///:memory:"
    
    # CORS
    ALLOWED_ORIGINS: list[str] = ["*"]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True
    )

# Global settings instance
settings = Settings()
