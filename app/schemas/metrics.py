from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class MetricQueryParams(BaseModel):
    tenant_id: str
    bucket_size: Literal["minute", "hour"] = "minute"
    source: str | None = None
    event_type: str | None = None
    from_ts: datetime | None = Field(None, alias="from")
    to_ts: datetime | None = Field(None, alias="to")


class MetricResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    tenant_id: str
    bucket_size: str
    source: str | None = None
    event_type: str | None = None
