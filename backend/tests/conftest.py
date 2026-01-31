import os

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# Set test environment variables before importing app modules
os.environ["SECRET_KEY"] = "test-secret-key-for-testing-only-do-not-use-in-production"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"

from app.database import get_session
from app.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=True,
    future=True,
)

test_session_maker = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def override_get_session():
    async with test_session_maker() as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


@pytest.fixture(scope="function")
async def async_client():
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client

    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
