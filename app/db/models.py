from datetime import UTC, datetime

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Index,
    String,
)
from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    pass


class Event(BaseModel):
    __tablename__ = "events"

    event_id = Column(String, primary_key=True)
    tenant_id = Column(String, nullable=False)
    source = Column(String)
    event_type = Column(String)
    timestamp = Column(DateTime, nullable=False)
    payload = Column(JSON)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))

    __table_args__ = (
        Index("idx_events_tenant_time", "tenant_id", "timestamp"),
        Index("idx_events_filters", "tenant_id", "source", "event_type"),
    )
