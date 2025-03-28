"""
NoteKo API - Main application entry point.
"""
import time
import logging
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1 import auth
from app.core.config import settings
from app.core.metadata import metadata
from app.core.health import check_database, get_system_info, check_middleware_status
from app.security.middleware import RateLimitMiddleware
from app.db.database import engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=metadata.name,
    description=metadata.get("description"),
    version=metadata.api_version
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
    # Get system information
    sys_info = get_system_info()
    startup_time = datetime.now()
    
    # Check database status
    db_status = await check_database(engine)
    
    # Check middleware status
    middleware_status = check_middleware_status(app)
    
    # ASCII art banner
    banner = """
    ███╗   ██╗ ██████╗ ████████╗███████╗██╗  ██╗ ██████╗ 
    ████╗  ██║██╔═══██╗╚══██╔══╝██╔════╝██║ ██╔╝██╔═══██╗
    ██╔██╗ ██║██║   ██║   ██║   █████╗  █████╔╝ ██║   ██║
    ██║╚██╗██║██║   ██║   ██║   ██╔══╝  ██╔═██╗ ██║   ██║
    ██║ ╚████║╚██████╔╝   ██║   ███████╗██║  ██╗╚██████╔╝
    ╚═╝  ╚═══╝ ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝ ╚═════╝ 
    """
    
    env_info = metadata.environment
    startup_message = f"""
{banner}
{'='*80}
{metadata.name} API Server
{'='*80}

VERSION INFORMATION
------------------
Application Version: {metadata.version}
API Version: {metadata.api_version}
Environment: {settings.ENVIRONMENT}

SYSTEM STATUS
------------
Python Runtime: {sys_info['python_version']}
Platform: {sys_info['platform']}
Framework: {env_info['framework']['name']} {env_info['framework']['version']}
Startup Time: {startup_time.strftime('%Y-%m-%d %H:%M:%S')}

DATABASE STATUS
--------------
Type: {env_info['database']['type']} {env_info['database']['version']}
Status: {db_status['status']}
{f"Message: {db_status['message']}" if db_status['status'] == 'offline' else ''}

MIDDLEWARE STATUS
---------------
CORS: {middleware_status['cors']}
Rate Limiting: {middleware_status['rate_limit']}
Authentication: JWT (Enabled)

DOCUMENTATION
------------
OpenAPI: {metadata.get('documentation', {}).get('openapi', '/docs')}
ReDoc: {metadata.get('documentation', {}).get('redoc', '/redoc')}
API Base URL: {metadata.get('api', {}).get('baseUrl', '/v1')}

{'='*80}
"""
    logger.info("\n" + startup_message)

@app.get("/")
async def root():
    """
    Root endpoint - displays welcome message.
    """
    return {
        "name": metadata.name,
        "version": metadata.version,
        "api_version": metadata.api_version,
        "status": "operational",
        "timestamp": int(time.time())
    }
