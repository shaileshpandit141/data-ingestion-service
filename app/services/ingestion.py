from datetime import UTC

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Event
from app.schemas.event import EventCreate


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
