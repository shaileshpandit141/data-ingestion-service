from collections.abc import Sequence

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Event
from app.schemas.event import EventQueryParams


async def get_events(db: AsyncSession, params: EventQueryParams) -> Sequence[Event]:
    filters = [Event.tenant_id == params.tenant_id]

    if params.source:
        filters.append(Event.source == params.source)

    if params.event_type:
        filters.append(Event.event_type == params.event_type)

    if params.from_ts:
        filters.append(Event.timestamp >= params.from_ts)

    if params.to_ts:
        filters.append(Event.timestamp <= params.to_ts)

    query = (
        select(Event)
        .where(and_(*filters))
        .order_by(Event.timestamp.asc(), Event.event_id.asc())
        .limit(params.limit)
        .offset(params.offset)
    )

    result = await db.execute(query)
    events = result.scalars().all()

    return events
