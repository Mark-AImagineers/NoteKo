"""
User-related Pydantic schemas.
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime

class UserBase(BaseModel):
    """Base user schema."""
    email: EmailStr
    
    model_config = ConfigDict(from_attributes=True)

class UserCreate(UserBase):
    """Schema for user creation."""
    password: str

class UserLogin(UserBase):
    """Schema for user login."""
    password: str

class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
