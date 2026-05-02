from datetime import UTC, datetime

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


async def run_aggregation(db: AsyncSession) -> None:
    """
    Incrementally aggregates events into aggregates table
    """

    # Get last processed timestamp
    result = await db.execute(
        text("SELECT last_processed_at FROM aggregation_state WHERE id='default'")
    )
    row = result.fetchone()

    last_processed = row[0] if row else None

    if last_processed is None:
        last_processed = datetime(1970, 1, 1)

    # Aggregate new events (minute-level)
    aggregation_query = text("""
        INSERT INTO aggregates (
            tenant_id,
            bucket_start,
            bucket_size,
            source,
            event_type,
            count,
            first_seen,
            last_seen
        )
        SELECT
            tenant_id,
            date_trunc('minute', timestamp) AS bucket_start,
            'minute',
            source,
            event_type,
            COUNT(*) AS count,
            MIN(timestamp),
            MAX(timestamp)
        FROM events
        WHERE timestamp > :last_processed
        GROUP BY tenant_id, bucket_start, source, event_type
        ON CONFLICT (tenant_id, bucket_start, bucket_size, source, event_type)
        DO UPDATE SET
            count = aggregates.count + EXCLUDED.count,
            last_seen = GREATEST(aggregates.last_seen, EXCLUDED.last_seen)
    """)

    await db.execute(aggregation_query, {"last_processed": last_processed})

    # Update state
    now = datetime.now(UTC)

    await db.execute(
        text("""
        INSERT INTO aggregation_state (id, last_processed_at)
        VALUES ('default', :now)
        ON CONFLICT (id)
        DO UPDATE SET last_processed_at = :now
    """),
        {"now": now},
    )

    await db.commit()
