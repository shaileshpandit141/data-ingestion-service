import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_bulk_ingestion(async_client: AsyncClient) -> None:
    payload = {
        "events": [
            {
                "event_id": f"evt_{i}",
                "tenant_id": "tenant_1",
                "timestamp": "2026-05-02T10:00:00Z",
            }
            for i in range(10)
        ]
    }

    res = await async_client.post("/events/bulk", json=payload)
    data = res.json()

    assert data["inserted"] == 10
    assert data["duplicates"] == 0
