from collections.abc import AsyncGenerator, Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

from .models import BaseDeclarativeModel

settings = get_settings()


async_engine = create_async_engine(
    url=settings.db.async_url,
    echo=settings.app.DEBUG,
    pool_pre_ping=True,
)

sync_engine = create_engine(
    url=settings.db.sync_url,
    echo=settings.app.DEBUG,
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    class_=Session,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def init_async_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(BaseDeclarativeModel.metadata.create_all)


def init_sync_db() -> None:
    with sync_engine.begin():
        BaseDeclarativeModel.metadata.create_all(sync_engine)


async def get_async_session() -> AsyncGenerator[AsyncSession]:
    async with AsyncSessionLocal() as session:
        yield session


def get_sync_session() -> Generator[Session]:
    with SyncSessionLocal() as session:
        yield session
