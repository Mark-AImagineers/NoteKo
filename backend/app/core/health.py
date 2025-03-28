"""
Health check utilities for system components.
"""
import sys
import platform
from datetime import datetime
from typing import Dict, Any
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy import text

async def check_database(engine: AsyncEngine) -> Dict[str, Any]:
    """Check database connection and return status."""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
            return {
                "status": "online",
                "message": "Connected successfully"
            }
    except Exception as e:
        return {
            "status": "offline",
            "message": str(e)
        }

def get_system_info() -> Dict[str, Any]:
    """Get system information."""
    return {
        "python_version": sys.version.split()[0],
        "platform": platform.platform(),
        "processor": platform.processor() or "Unknown",
        "cpu_count": platform.machine(),
        "timestamp": datetime.now().isoformat()
    }

def check_middleware_status(app) -> Dict[str, str]:
    """Check middleware status."""
    middleware_status = {}
    
    # Get all middleware
    middleware_stack = app.user_middleware if hasattr(app, 'user_middleware') else []
    
    # Check CORS
    cors_enabled = any(
        "CORSMiddleware" in str(m.cls) 
        for m in middleware_stack
    )
    middleware_status["cors"] = "enabled" if cors_enabled else "disabled"
    
    # Check Rate Limiting
    rate_limit_enabled = any(
        "RateLimitMiddleware" in str(m.cls)
        for m in middleware_stack
    )
    middleware_status["rate_limit"] = "enabled" if rate_limit_enabled else "disabled"
    
    return middleware_status
