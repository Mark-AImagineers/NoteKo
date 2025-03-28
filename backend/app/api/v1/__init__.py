"""
API v1 router configuration.
"""
from fastapi import APIRouter
from .auth import router as auth_router

router = APIRouter(prefix="/v1")

# Include routers
router.include_router(auth_router)
