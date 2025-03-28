"""
Test configuration and fixtures.
"""
import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.pool import NullPool

from app.main import app
from app.db.database import Base, get_db
from app.models.user import User
from app.core.config import settings

# Test database URL
TEST_SCHEMA = "test"

@pytest.fixture(scope="session")
async def test_engine():
    """Create a test database engine."""
    engine = create_async_engine(
        settings.DATABASE_URL,
        poolclass=NullPool,
        connect_args={"server_settings": {"search_path": TEST_SCHEMA}},
        echo=True,
    )
    
    async with engine.begin() as conn:
        # Create test schema
        await conn.execute(text(f"DROP SCHEMA IF EXISTS {TEST_SCHEMA} CASCADE"))
        await conn.execute(text(f"CREATE SCHEMA {TEST_SCHEMA}"))
        
        # Create tables in test schema
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Clean up test schema
    async with engine.begin() as conn:
        await conn.execute(text(f"DROP SCHEMA IF EXISTS {TEST_SCHEMA} CASCADE"))
    
    await engine.dispose()

@pytest.fixture
async def test_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create a test database session."""
    async_session = sessionmaker(
        test_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )
    
    async with async_session() as session:
        async with session.begin():
            # Clear all tables before each test
            for table in reversed(Base.metadata.sorted_tables):
                await session.execute(table.delete())
        
        yield session
        await session.rollback()

@pytest.fixture
async def override_get_db(test_session):
    """Override the database dependency."""
    async def _override_get_db():
        yield test_session

    app.dependency_overrides[get_db] = _override_get_db
    yield test_session
    app.dependency_overrides.clear()
