from collections.abc import AsyncGenerator
from typing import Any

import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.db.models import BaseModel
from app.db.session import get_async_session
from app.main import app

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


@pytest_asyncio.fixture(scope="session")
async def async_engine() -> AsyncGenerator[AsyncEngine]:
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def async_session(
    async_engine: AsyncEngine,
) -> AsyncGenerator[AsyncSession]:
    async_session = async_sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        try:
            yield session
        finally:
            await session.rollback()


@pytest_asyncio.fixture
async def async_client(async_session: AsyncSession) -> AsyncGenerator[AsyncClient, Any]:
    async def get_async_test_session() -> AsyncGenerator[AsyncSession, Any]:
        yield async_session

    app.dependency_overrides[get_async_session] = get_async_test_session

    transport = ASGITransport(app=app)

    async with AsyncClient(transport=transport, base_url="http://test") as async_client:
        yield async_client

    app.dependency_overrides.clear()
