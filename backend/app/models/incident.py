from datetime import UTC, datetime

from sqlalchemy import DateTime, Enum, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import IncidentSeverity, IncidentStatus, enum_values


class Incident(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "incidents"

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        index=True,
    )
    service_id: Mapped[str | None] = mapped_column(
        ForeignKey("deployable_services.id", ondelete="SET NULL"),
        index=True,
    )
    environment_id: Mapped[str | None] = mapped_column(
        ForeignKey("service_environments.id", ondelete="SET NULL"),
        index=True,
    )
    deployment_id: Mapped[str | None] = mapped_column(
        ForeignKey("deployments.id", ondelete="SET NULL"),
        index=True,
    )
    title: Mapped[str] = mapped_column(String(240), index=True)
    severity: Mapped[IncidentSeverity] = mapped_column(
        Enum(IncidentSeverity, values_callable=enum_values, native_enum=False),
        nullable=False,
        index=True,
    )
    status: Mapped[IncidentStatus] = mapped_column(
        Enum(IncidentStatus, values_callable=enum_values, native_enum=False),
        default=IncidentStatus.OPEN,
        nullable=False,
        index=True,
    )
    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))


class IncidentTimelineEntry(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "incident_timeline_entries"

    incident_id: Mapped[str] = mapped_column(
        ForeignKey("incidents.id", ondelete="CASCADE"),
        index=True,
    )
    actor_id: Mapped[str | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        index=True,
    )
    message: Mapped[str] = mapped_column(Text)
