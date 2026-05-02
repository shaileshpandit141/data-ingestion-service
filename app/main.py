from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from sqlalchemy import text

from .core.config import get_settings
from .core.lifespan import lifespan
from .db.session import async_engine

settings = get_settings()


app = FastAPI(
    title=settings.app.NAME,
    debug=settings.app.DEBUG,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors.ALLOW_ORIGINS,
    allow_methods=settings.cors.ALLOW_METHODS,
    allow_headers=settings.cors.ALLOW_HEADERS,
    allow_credentials=settings.cors.ALLOW_CREDENTIALS,
)


@app.get(path="/", include_in_schema=False)
def root(request: Request) -> RedirectResponse:
    return RedirectResponse(url="/docs", status_code=307)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get(
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
