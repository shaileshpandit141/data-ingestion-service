from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.db.session import async_engine, init_async_db

from .config import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    # ---- Startup ----
    print("Starting application...")

    try:
        # Initialize database (migrations, tables, etc.)
        await init_async_db()
        print("Database initialized successfully.")

        yield
    except Exception as exc:
        print(f"Application startup failed.  \nError: {str(exc)}")
        raise

    finally:
        # ---- Shutdown ----
        print("Shutting down application...")
        try:
            await async_engine.dispose()
            print("Database engine disposed.")
        except Exception as exc:
            print(f"Error disposing database engine. \nError: {str(exc)}")

        print("Resources cleaned up successfully.")
