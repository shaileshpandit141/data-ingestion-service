import asyncio
from typing import NoReturn

from app.db.session import AsyncSessionLocal
from app.services.aggregation import run_aggregation

AGGREGATION_INTERVAL = 10  # seconds


async def aggregation_worker() -> NoReturn:
    while True:
        try:
            async with AsyncSessionLocal() as db:
                await run_aggregation(db)

        except Exception as exc:
            print(f"[Aggregation Worker Error] {exc}")

        await asyncio.sleep(AGGREGATION_INTERVAL)
