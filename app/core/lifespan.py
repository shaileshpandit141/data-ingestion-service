import asyncio
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager, suppress

from fastapi import FastAPI

from app.db.session import async_engine, init_async_db
from app.worker import aggregation_worker

from .config import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    print("Starting application...")

    task: asyncio.Task[None] | None = None

    try:
        # Initialize DB first
        await init_async_db()
        print("Database initialized successfully.")

        # Start worker after DB is ready
        task = asyncio.create_task(aggregation_worker())

        yield

    except Exception as exc:
        print(f"Application startup failed.\nError: {exc}")
        raise

    finally:
        print("Shutting down application...")

        # Stop worker safely
        if task:
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task

        # Dispose DB engine
        try:
            await async_engine.dispose()
            print("Database engine disposed.")
        except Exception as exc:
            print(f"Error disposing database engine.\nError: {exc}")

        print("Resources cleaned up successfully.")
