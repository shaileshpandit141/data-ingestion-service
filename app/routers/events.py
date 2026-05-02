from collections.abc import Sequence
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.schemas.event import (
    BulkEventCreate,
    EventCreate,
    EventQueryParams,
    EventResponse,
)
from app.services.ingestion import bulk_insert_events, insert_event
from app.services.query import get_events

router = APIRouter()


@router.post("/events", responses={400: {"description": "Bad Request"}})
async def create_event(
    event: EventCreate, db: Annotated[AsyncSession, Depends(get_async_session)]
) -> dict[str, str]:
    try:
        inserted = await insert_event(db, event)

        if not inserted:
            return {
                "status": "duplicate",
                "event_id": event.event_id,
            }

        return {
            "status": "created",
            "event_id": event.event_id,
        }
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/events/bulk", responses={400: {"description": "Bad Request"}})
async def bulk_create_events(
    payload: BulkEventCreate, db: Annotated[AsyncSession, Depends(get_async_session)]
) -> dict[str, Any]:
    try:
        result = await bulk_insert_events(db, payload.events)
        return {"status": "success", **result}

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/events")
async def list_events(
    params: Annotated[EventQueryParams, Depends()],
    db: Annotated[AsyncSession, Depends(get_async_session)],
) -> dict[str, int | Sequence[EventResponse]]:
    events = await get_events(db, params)

    return {
        "count": len(events),
        "items": events,  # type: ignore
    }
