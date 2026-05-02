from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, Field


class EventCreate(BaseModel):
    event_id: str
    tenant_id: str
    source: str | None = None
    event_type: str | None = None
    timestamp: datetime
    payload: dict[str, Any] | None = None

    # Enforce UTC
    def validate_timestamp(self) -> datetime:
        if self.timestamp.tzinfo is None:
            raise ValueError("timestamp must be timezone-aware (UTC required)")
        return self.timestamp.astimezone(UTC)


class BulkEventCreate(BaseModel):
    events: list[EventCreate] = Field(..., min_length=1, max_length=5000)


class EventQueryParams(BaseModel):
    tenant_id: str
    source: str | None = None
    event_type: str | None = None
    from_ts: datetime | None = Field(None, alias="from")
    to_ts: datetime | None = Field(None, alias="to")

    limit: int = Field(50, le=100)
    offset: int = 0
