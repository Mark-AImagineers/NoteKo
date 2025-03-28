"""
Token-related Pydantic schemas.
"""
from typing import Optional
from pydantic import BaseModel, ConfigDict

class Token(BaseModel):
    """Schema for token response."""
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    
    model_config = ConfigDict(from_attributes=True)

class TokenPayload(BaseModel):
    sub: str  # Subject (user id)
    exp: int  # Expiration time
    iat: int  # Issued at
    type: str  # Token type (access or refresh)
