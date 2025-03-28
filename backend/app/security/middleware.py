"""
Security middleware implementing industry-standard protection mechanisms.
Includes rate limiting, security headers, and authentication dependencies.
"""
from fastapi import HTTPException, Security, Depends
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import time
from typing import Optional, Dict
from app.auth.jwt import jwt_auth

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware to prevent brute force attacks.
    Uses a simple in-memory store (should use Redis in production).
    """
    def __init__(self, app, calls: int = 60, period: int = 60):
        super().__init__(app)
        self.calls = calls  # Number of calls allowed
        self.period = period  # Time period in seconds
        self.store: Dict[str, list] = {}  # Store IP -> [timestamp, timestamp, ...]

    async def dispatch(self, request: Request, call_next) -> Response:
        # Get client IP or use default for testing
        ip = "test" if request.client is None else request.client.host
        now = time.time()
        
        # Initialize or clean old requests
        if ip not in self.store:
            self.store[ip] = []
        self.store[ip] = [ts for ts in self.store[ip] if now - ts < self.period]
        
        # Check rate limit
        if len(self.store[ip]) >= self.calls:
            raise HTTPException(
                status_code=429,
                detail="Too many requests"
            )
        
        # Add request timestamp
        self.store[ip].append(now)
        
        # Add security headers
        response = await call_next(request)
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Optional[Dict]:
    """
    Dependency to get current authenticated user from JWT token.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = jwt_auth.verify_token(token)
    if payload is None:
        raise credentials_exception
        
    return payload
