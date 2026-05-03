import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_idempotent_event_ingestion(async_client: AsyncClient) -> None:
    payload = {
        "event_id": "evt_test_1",
        "tenant_id": "tenant_100",
        "timestamp": "2026-05-02T10:00:00Z",
    }

    res1 = await async_client.post("/events", json=payload)
    res2 = await async_client.post("/events", json=payload)

    assert res1.json()["status"] == "created"
    assert res2.json()["status"] == "duplicate"
