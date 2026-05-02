from collections.abc import Sequence

from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Aggregate
from app.schemas.metrics import MetricQueryParams


async def get_metrics(
    db: AsyncSession, params: MetricQueryParams
) -> Sequence[Aggregate]:
    filters = [
        Aggregate.tenant_id == params.tenant_id,
        Aggregate.bucket_size == params.bucket_size,
    ]

    if params.from_ts:
        filters.append(
            Aggregate.bucket_start >= params.from_ts,
        )

    if params.to_ts:
        filters.append(
            Aggregate.bucket_start <= params.to_ts,
        )

    if params.source:
        filters.append(
            Aggregate.source == params.source,
        )

    if params.event_type:
        filters.append(
            Aggregate.event_type == params.event_type,
        )

    query = (
        select(Aggregate)
        .where(and_(*filters))
        .order_by(
            Aggregate.bucket_start.asc(),
        )
    )

    result = await db.execute(query)
    return result.scalars().all()
