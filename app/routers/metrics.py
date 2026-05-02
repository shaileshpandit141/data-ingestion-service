from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.schemas.metrics import MetricQueryParams, MetricResponse
from app.services.metrics import get_metrics

router = APIRouter()


@router.get("/metrics")
async def metrics(
    params: Annotated[MetricQueryParams, Depends()],
    db: Annotated[AsyncSession, Depends(get_async_session)],
) -> dict[str, int | Sequence[MetricResponse]]:
    data = await get_metrics(db, params)

    return {"count": len(data), "items": data}  # type: ignore
