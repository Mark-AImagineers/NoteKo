"""
JWT authentication handler implementing token-based user authentication.
"""
from datetime import timedelta
from typing import Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from app.db.database import get_db
from app.models.user import User
from app.security import (
    verify_password,
    create_access_token,
    create_refresh_token,
    get_current_user
)

class JWTAuth:
    """
    Handles JWT authentication and token management.
    """
    def __init__(self):
        self.get_current_user = get_current_user

    async def authenticate_user(
        self,
        email: str,
        password: str,
        db: AsyncSession
    ) -> Optional[User]:
        """
        Authenticate a user by email and password.
        Returns None if authentication fails.
        """
        # Get user by email
        query = await db.execute(User.__table__.select().where(User.email == email))
        user = query.first()
        
        if not user:
            return None
            
        # Verify password
        if not verify_password(password, user.hashed_password):
            return None
            
        return user

    async def create_tokens(
        self,
        user_id: int,
        expires_delta: Optional[timedelta] = None
    ) -> Tuple[str, str]:
        """
        Create new access and refresh tokens for a user.
        """
        # Create token data
        token_data = {"sub": str(user_id)}
        
        # Generate tokens
        access_token = create_access_token(
            data=token_data,
            expires_delta=expires_delta
        )
        refresh_token = create_refresh_token(data=token_data)
        
        return access_token, refresh_token

# Create global instance
jwt_auth = JWTAuth()
