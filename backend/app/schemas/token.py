"""
Token-related Pydantic schemas.
"""
from pydantic import BaseModel, ConfigDict

class Token(BaseModel):
    """Schema for token response."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    
    model_config = ConfigDict(from_attributes=True)

class TokenPayload(BaseModel):
    sub: str  # Subject (user id)
    exp: int  # Expiration time
    iat: int  # Issued at
    type: str  # Token type (access or refresh)
