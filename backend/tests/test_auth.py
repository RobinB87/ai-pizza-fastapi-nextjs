import pytest


@pytest.mark.asyncio
async def test_register_user(async_client):
    """Test user registration."""
    response = await async_client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["is_active"] is True
    assert data["is_superuser"] is False
    assert "id" in data
    assert "hashed_password" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(async_client):
    """Test registration with duplicate email fails."""
    await async_client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    response = await async_client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "anotherpassword"},
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


@pytest.mark.asyncio
async def test_login_success(async_client):
    """Test successful login."""
    await async_client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    response = await async_client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(async_client):
    """Test login with wrong password fails."""
    await async_client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    response = await async_client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


@pytest.mark.asyncio
async def test_login_nonexistent_user(async_client):
    """Test login with nonexistent user fails."""
    response = await async_client.post(
        "/auth/login",
        json={"email": "nonexistent@example.com", "password": "testpassword123"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


@pytest.mark.asyncio
async def test_get_current_user(async_client):
    """Test getting current user info with token."""
    await async_client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    login_response = await async_client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    token = login_response.json()["access_token"]

    response = await async_client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"


@pytest.mark.asyncio
async def test_get_current_user_invalid_token(async_client):
    """Test getting current user with invalid token fails."""
    response = await async_client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_route_without_token(async_client):
    """Test protected route without token fails."""
    response = await async_client.post(
        "/pizzerias",
        json={"name": "Test Pizza", "address": "123 Test St"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_protected_route_with_token(async_client):
    """Test protected route with valid token succeeds."""
    await async_client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    login_response = await async_client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    token = login_response.json()["access_token"]

    response = await async_client.post(
        "/pizzerias",
        json={"name": "Test Pizza", "address": "123 Test St"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Pizza"


@pytest.mark.asyncio
async def test_refresh_token(async_client):
    """Test token refresh."""
    await async_client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    login_response = await async_client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    refresh_token = login_response.json()["refresh_token"]

    response = await async_client.post(
        "/auth/refresh",
        json={"refresh_token": refresh_token},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


@pytest.mark.asyncio
async def test_refresh_token_invalid(async_client):
    """Test refresh with invalid token fails."""
    response = await async_client.post(
        "/auth/refresh",
        json={"refresh_token": "invalid-refresh-token"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_refresh_with_access_token_fails(async_client):
    """Test refresh using access token instead of refresh token fails."""
    await async_client.post(
        "/auth/register",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    login_response = await async_client.post(
        "/auth/login",
        json={"email": "test@example.com", "password": "testpassword123"},
    )
    access_token = login_response.json()["access_token"]

    response = await async_client.post(
        "/auth/refresh",
        json={"refresh_token": access_token},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token type"


@pytest.mark.asyncio
async def test_public_routes_without_auth(async_client):
    """Test public routes work without authentication."""
    response = await async_client.get("/")
    assert response.status_code == 200

    response = await async_client.get("/pizzerias")
    assert response.status_code == 200
