from fastapi import APIRouter, HTTPException
from sqlalchemy import text

from app.db.session import async_engine

router = APIRouter()


@router.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get(
    "/ready",
    responses={
        503: {
            "description": "Service unavailable - database disconnected",
        }
    },
)
async def ready() -> dict[str, str]:
    try:
        async with async_engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "error",
                "database": "disconnected",
            },
        ) from exc
