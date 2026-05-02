from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.schemas.event import EventCreate
from app.services.ingestion import insert_event

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
