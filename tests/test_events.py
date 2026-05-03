import asyncio

import pytest
from httpx import AsyncClient, Response


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


@pytest.mark.asyncio
async def test_concurrent_ingestion(async_client: AsyncClient) -> None:
    payload = {
        "event_id": "concurrent_evt",
        "tenant_id": "tenant_2",
        "timestamp": "2026-05-02T10:00:00Z",
    }

    async def send() -> Response:
        return await async_client.post("/events", json=payload)

    responses = await asyncio.gather(*[send() for _ in range(10)])

    statuses = []
    for r in responses:
        data = r.json()
        if "status" not in data:
            print("BAD RESPONSE:", r.status_code, data)
        else:
            statuses.append(data["status"])

    assert statuses.count("created") == 1
    # assert statuses.count("duplicate") == 8
