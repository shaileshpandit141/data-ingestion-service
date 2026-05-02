from datetime import UTC
from typing import Any

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Event
from app.schemas.event import EventCreate

CHUNK_SIZE = 1000


async def insert_event(db: AsyncSession, event: EventCreate) -> bool:
    """
    Returns True if inserted, False if duplicate
    """

    # Ensure UTC
    if event.timestamp.tzinfo is None:
        raise ValueError("Timestamp must be timezone-aware")

    stmt = (
        insert(Event)
        .values(
            event_id=event.event_id,
            tenant_id=event.tenant_id,
            source=event.source,
            event_type=event.event_type,
            timestamp=event.timestamp.astimezone(UTC),
            payload=event.payload,
        )
        .on_conflict_do_nothing(index_elements=["event_id"])
    )

    result = await db.execute(stmt)
    await db.commit()

    # If rowcount == 0 → duplicate
    return result.rowcount > 0  # type: ignore


async def bulk_insert_events(
    db: AsyncSession, events: list[EventCreate]
) -> dict[str, Any | int]:
    total_inserted = 0
    total_duplicates = 0

    # Convert to dicts
    processed_events: list[Any] = []

    for event in events:
        if event.timestamp.tzinfo is None:
            raise ValueError("All timestamps must be timezone-aware")

        processed_events.append(
            {
                "event_id": event.event_id,
                "tenant_id": event.tenant_id,
                "source": event.source,
                "event_type": event.event_type,
                "timestamp": event.timestamp.astimezone(UTC),
                "payload": event.payload,
            }
        )

    # Chunk processing
    for i in range(0, len(processed_events), CHUNK_SIZE):
        chunk = processed_events[i : i + CHUNK_SIZE]

        stmt = (
            insert(Event)
            .values(chunk)
            .on_conflict_do_nothing(index_elements=["event_id"])
        )

        result = await db.execute(stmt)

        inserted = result.rowcount or 0  # type: ignore
        total_inserted += inserted
        total_duplicates += len(chunk) - inserted

    await db.commit()

    return {
        "inserted": total_inserted,
        "duplicates": total_duplicates,
        "total": len(events),
    }
