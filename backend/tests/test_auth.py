"""
Tests for authentication endpoints.
"""
import pytest
from datetime import datetime, timedelta
import jwt
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.models.user import User
from app.auth.jwt import jwt_auth
from app.security import get_password_hash

pytestmark = pytest.mark.asyncio

# Test data
TEST_USER = {
    "email": "test@example.com",
    "password": "Test123!@#"
}

@pytest.fixture
async def async_client(override_get_db):
    """Async client fixture."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as client:
        yield client

@pytest.fixture
async def test_user(test_session):
    """Create a test user and return their credentials."""
    db_user = User(
        email=TEST_USER["email"],
        hashed_password=get_password_hash(TEST_USER["password"])
    )
    test_session.add(db_user)
    await test_session.commit()
    await test_session.refresh(db_user)
    return db_user

@pytest.fixture
async def auth_headers(test_user):
    """Get authentication headers for test user."""
    access_token = jwt_auth.create_access_token(data={"sub": test_user.email})
    return {"Authorization": f"Bearer {access_token}"}

# Registration Tests
async def test_register_user_success(async_client):
    """Test successful user registration."""
    response = await async_client.post(
        "/v1/auth/register",
        json={
            "email": "new@example.com",
            "password": "Test123!@#"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "new@example.com"
    assert "id" in data
    assert data["is_active"] is True
    assert "hashed_password" not in data

async def test_register_invalid_email(async_client):
    """Test registration with invalid email format."""
    response = await async_client.post(
        "/v1/auth/register",
        json={
            "email": "invalid-email",
            "password": "Test123!@#"
        }
    )
    assert response.status_code == 422

async def test_register_weak_password(async_client):
    """Test registration with weak password."""
    response = await async_client.post(
        "/v1/auth/register",
        json={
            "email": "weak@example.com",
            "password": "weak"
        }
    )
    assert response.status_code == 400
    assert "password" in response.json()["detail"].lower()

async def test_register_duplicate_email(async_client, test_user):
    """Test registration with duplicate email."""
    response = await async_client.post(
        "/v1/auth/register",
        json=TEST_USER
    )
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()

# Login Tests
async def test_login_success(async_client, test_user):
    """Test successful login."""
    response = await async_client.post(
        "/v1/auth/login",
        json=TEST_USER
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

async def test_login_invalid_email(async_client):
    """Test login with non-existent email."""
    response = await async_client.post(
        "/v1/auth/login",
        json={
            "email": "nonexistent@example.com",
            "password": "Test123!@#"
        }
    )
    assert response.status_code == 401
    assert "invalid email or password" in response.json()["detail"].lower()

async def test_login_wrong_password(async_client, test_user):
    """Test login with wrong password."""
    response = await async_client.post(
        "/v1/auth/login",
        json={
            "email": TEST_USER["email"],
            "password": "WrongPass123!"
        }
    )
    assert response.status_code == 401
    assert "invalid email or password" in response.json()["detail"].lower()

# Token Tests
async def test_refresh_token_success(async_client, test_user):
    """Test successful token refresh."""
    # First login to get tokens
    login_response = await async_client.post(
        "/v1/auth/login",
        json=TEST_USER
    )
    refresh_token = login_response.json()["refresh_token"]
    
    # Use refresh token to get new access token
    response = await async_client.post(
        "/v1/auth/refresh",
        headers={"Authorization": f"Bearer {refresh_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["refresh_token"] is None
    assert data["token_type"] == "bearer"

async def test_refresh_token_with_access_token(async_client, auth_headers):
    """Test refresh token endpoint with access token (should fail)."""
    response = await async_client.post(
        "/v1/auth/refresh",
        headers=auth_headers
    )
    assert response.status_code == 401

async def test_refresh_token_expired(async_client, test_user):
    """Test refresh with expired token."""
    # Create an expired refresh token
    expired_token = jwt_auth.create_refresh_token(
        data={"sub": test_user.email},
        expires_delta=timedelta(minutes=-1)
    )
    
    response = await async_client.post(
        "/v1/auth/refresh",
        headers={"Authorization": f"Bearer {expired_token}"}
    )
    assert response.status_code == 401
    assert "expired" in response.json()["detail"].lower()

# User Info Tests
async def test_get_user_info_success(async_client, auth_headers):
    """Test getting user info with valid token."""
    response = await async_client.get(
        "/v1/auth/me",
        headers=auth_headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == TEST_USER["email"]
    assert "hashed_password" not in data

async def test_get_user_info_no_token(async_client):
    """Test getting user info without token."""
    response = await async_client.get("/v1/auth/me")
    assert response.status_code == 401

async def test_get_user_info_invalid_token(async_client):
    """Test getting user info with invalid token."""
    response = await async_client.get(
        "/v1/auth/me",
        headers={"Authorization": "Bearer invalid-token"}
    )
    assert response.status_code == 401
