import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.aggregation import run_aggregation


@pytest.mark.asyncio
@pytest.mark.skip
async def test_metrics_aggregation(
    async_client: AsyncClient, async_session: AsyncSession
) -> None:
    # Insert events
    for i in range(5):
        await async_client.post(
            "/events",
            json={
                "event_id": f"agg_evt_{i}",
                "tenant_id": "tenant_agg",
                "timestamp": "2026-05-02T10:00:00Z",
            },
        )

    # aggregation
    await run_aggregation(async_session)

    res = await async_client.get("/metrics?tenant_id=tenant_agg&bucket_size=minute")
    data = res.json()

    assert data["count"] >= 1
