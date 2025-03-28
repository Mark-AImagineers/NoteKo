"""
Tests for authentication endpoints.
"""
import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

pytestmark = pytest.mark.asyncio

@pytest.fixture
async def async_client(override_get_db):
    """Async client fixture."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

async def test_register_user(async_client):
    """Test user registration endpoint."""
    response = await async_client.post(
        "/v1/auth/register",
        json={
            "email": "test@example.com",
            "password": "Test123!@#"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert data["is_active"] is True

async def test_register_duplicate_email(async_client):
    """Test registration with duplicate email."""
    # First registration
    await async_client.post(
        "/v1/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "Test123!@#"
        }
    )
    
    # Attempt duplicate registration
    response = await async_client.post(
        "/v1/auth/register",
        json={
            "email": "duplicate@example.com",
            "password": "Test123!@#"
        }
    )
    assert response.status_code == 400
    assert "Email already registered" in response.json()["detail"]

async def test_login_success(async_client):
    """Test successful login."""
    # Register user first
    await async_client.post(
        "/v1/auth/register",
        json={
            "email": "login@example.com",
            "password": "Test123!@#"
        }
    )
    
    # Attempt login
    response = await async_client.post(
        "/v1/auth/login",
        json={
            "email": "login@example.com",
            "password": "Test123!@#"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

async def test_login_invalid_credentials(async_client):
    """Test login with invalid credentials."""
    response = await async_client.post(
        "/v1/auth/login",
        json={
            "email": "wrong@example.com",
            "password": "WrongPass123!"
        }
    )
    assert response.status_code == 401
    assert "Incorrect email or password" in response.json()["detail"]

async def test_get_user_info(async_client):
    """Test getting user info with valid token."""
    # Register and login user
    await async_client.post(
        "/v1/auth/register",
        json={
            "email": "info@example.com",
            "password": "Test123!@#"
        }
    )
    
    login_response = await async_client.post(
        "/v1/auth/login",
        json={
            "email": "info@example.com",
            "password": "Test123!@#"
        }
    )
    token = login_response.json()["access_token"]
    
    # Get user info
    response = await async_client.get(
        "/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "info@example.com"

async def test_refresh_token(async_client):
    """Test refresh token endpoint."""
    # Register and login user
    await async_client.post(
        "/v1/auth/register",
        json={
            "email": "refresh@example.com",
            "password": "Test123!@#"
        }
    )
    
    login_response = await async_client.post(
        "/v1/auth/login",
        json={
            "email": "refresh@example.com",
            "password": "Test123!@#"
        }
    )
    refresh_token = login_response.json()["refresh_token"]
    
    # Use refresh token to get new tokens
    response = await async_client.post(
        "/v1/auth/refresh",
        headers={"Authorization": f"Bearer {refresh_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
