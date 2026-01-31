import pytest


async def get_auth_header(async_client):
    """Helper to register and login a user, returning auth header."""
    await async_client.post(
        "/auth/register",
        json={"email": "testuser@example.com", "password": "testpassword123"},
    )
    login_response = await async_client.post(
        "/auth/login",
        json={"email": "testuser@example.com", "password": "testpassword123"},
    )
    token = login_response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_read_root(async_client):
    response = await async_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to AI Pizza API"}


@pytest.mark.asyncio
async def test_get_all_pizzerias_empty(async_client):
    response = await async_client.get("/pizzerias")
    assert response.status_code == 200
    pizzerias = response.json()
    assert isinstance(pizzerias, list)
    assert len(pizzerias) == 0


@pytest.mark.asyncio
async def test_create_pizzeria(async_client):
    auth_header = await get_auth_header(async_client)
    pizzeria_data = {
        "name": "Test Pizzeria",
        "address": "Test Street 123, Berlin",
        "rating": 4.5,
    }
    response = await async_client.post(
        "/pizzerias", json=pizzeria_data, headers=auth_header
    )
    assert response.status_code == 201

    pizzeria = response.json()
    assert pizzeria["name"] == "Test Pizzeria"
    assert pizzeria["address"] == "Test Street 123, Berlin"
    assert pizzeria["rating"] == 4.5
    assert "id" in pizzeria
    assert "created_at" in pizzeria


@pytest.mark.asyncio
async def test_create_and_get_pizzeria(async_client):
    auth_header = await get_auth_header(async_client)
    pizzeria_data = {
        "name": "Gazzo",
        "address": "Hobrechtstraße 57, 12047 Berlin",
        "rating": 4.7,
        "google_maps_url": "https://maps.google.com/?q=Gazzo+Berlin",
    }
    await async_client.post("/pizzerias", json=pizzeria_data, headers=auth_header)

    response = await async_client.get("/pizzerias")
    assert response.status_code == 200

    pizzerias = response.json()
    assert len(pizzerias) == 1
    assert pizzerias[0]["name"] == "Gazzo"
