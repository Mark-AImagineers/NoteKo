"""
Authentication endpoints for user registration, login, and token management.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.models.user import User
from app.schemas import (
    Token,
    UserCreate,
    UserLogin,
    UserResponse
)
from app.security import (
    get_password_hash,
    validate_password,
    get_current_user,
    verify_password
)
from app.auth.jwt import jwt_auth
from app.security.middleware import oauth2_scheme

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Register a new user.
    """
    # Check if email already exists
    query = await db.execute(
        User.__table__.select().where(User.email == user_data.email)
    )
    if query.first() is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Validate password
    is_valid, error_message = validate_password(user_data.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_message
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return new_user

@router.post("/login", response_model=Token)
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Authenticate user and return tokens.
    """
    # Find user by email
    query = await db.execute(
        User.__table__.select().where(User.email == user_data.email)
    )
    user = query.first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Verify password
    if not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Generate tokens
    access_token = jwt_auth.create_access_token(data={"sub": user.email})
    refresh_token = jwt_auth.create_refresh_token(data={"sub": user.email})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(
    token: str = Depends(oauth2_scheme)
):
    """
    Create new access token using refresh token.
    """
    # Verify refresh token
    payload = jwt_auth.verify_token(token, "refresh")
    
    # Create new access token
    access_token = jwt_auth.create_access_token(data={"sub": payload["sub"]})
    
    return {
        "access_token": access_token,
        "refresh_token": None,  # Don't refresh the refresh token
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
async def get_user_info(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    Get current user information.
    """
    query = await db.execute(
        User.__table__.select().where(User.email == current_user["sub"])
    )
    user = query.first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user
