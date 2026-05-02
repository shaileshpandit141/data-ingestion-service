from datetime import UTC, datetime
from typing import Any

from sqlalchemy import (
    JSON,
    DateTime,
    Index,
    Integer,
    PrimaryKeyConstraint,
    String,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class BaseModel(DeclarativeBase):
    pass


class Event(BaseModel):
    __tablename__ = "events"

    event_id: Mapped[str] = mapped_column(String, primary_key=True)
    tenant_id: Mapped[str] = mapped_column(String, nullable=False)
    source: Mapped[str | None] = mapped_column(String, nullable=True)
    event_type: Mapped[str | None] = mapped_column(String, nullable=True)
    payload: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(UTC)
    )

    __table_args__ = (
        Index("idx_events_tenant_time", "tenant_id", "timestamp"),
        Index("idx_events_filters", "tenant_id", "source", "event_type"),
    )


class Aggregate(BaseModel):
    __tablename__ = "aggregates"

    tenant_id: Mapped[str] = mapped_column(String)
    bucket_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    bucket_size: Mapped[str] = mapped_column(String)  # minute/hour
    source: Mapped[str] = mapped_column(String)
    event_type: Mapped[str] = mapped_column(String)

    count: Mapped[int] = mapped_column(Integer)
    first_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    last_seen: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        PrimaryKeyConstraint(
            "tenant_id",
            "bucket_start",
            "bucket_size",
            "source",
            "event_type",
        ),
    )


class AggregationState(BaseModel):
    __tablename__ = "aggregation_state"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default="default",
    )

    last_processed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
