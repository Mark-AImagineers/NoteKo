"""
NoteKo API - Main application entry point.
"""
import time
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth
from app.core.config import settings
from app.security.middleware import RateLimitMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="NoteKo API",
    description="A modern note-taking application API",
    version=settings.VERSION
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add rate limiting
app.add_middleware(RateLimitMiddleware)

# Include routers
app.include_router(auth.router, prefix="/v1")

@app.on_event("startup")
async def startup_event():
    """
    Handle application startup events.
    """
    # ASCII art banner
    banner = """
    ███╗   ██╗ ██████╗ ████████╗███████╗██╗  ██╗ ██████╗ 
    ████╗  ██║██╔═══██╗╚══██╔══╝██╔════╝██║ ██╔╝██╔═══██╗
    ██╔██╗ ██║██║   ██║   ██║   █████╗  █████╔╝ ██║   ██║
    ██║╚██╗██║██║   ██║   ██║   ██╔══╝  ██╔═██╗ ██║   ██║
    ██║ ╚████║╚██████╔╝   ██║   ███████╗██║  ██╗╚██████╔╝
    ╚═╝  ╚═══╝ ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝ ╚═════╝ 
    """
    
    startup_message = f"""
{banner}
{'='*80}
API Version: {settings.VERSION}
Environment: {settings.ENVIRONMENT}
Database: PostgreSQL
Authentication: JWT with Rate Limiting
{'='*80}

[*] Starting up NoteKo API service...
[*] Initializing database connection...
[*] Loading configuration...
[*] Setting up authentication...
[*] Starting API server...
[+] API server is ready!

Documentation: http://localhost:8000/docs
API Base URL: http://localhost:8000/v1
{'='*80}
"""
    logger.info("\n" + startup_message)

@app.get("/")
async def root():
    """
    Root endpoint - displays welcome message.
    """
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "operational",
        "timestamp": int(time.time())
    }
