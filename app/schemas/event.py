from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel


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
