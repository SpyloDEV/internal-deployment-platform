from datetime import datetime

from sqlalchemy import (
    Boolean,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import (
    DeploymentStatus,
    EnvironmentName,
    LogLevel,
    ServiceFramework,
    ServiceStatus,
    ServiceType,
    enum_values,
)


class Team(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "teams"
    __table_args__ = (UniqueConstraint("organization_id", "slug", name="uq_team_slug"),)

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        index=True,
    )
    name: Mapped[str] = mapped_column(String(180), index=True)
    slug: Mapped[str] = mapped_column(String(180), index=True)


class DeployableService(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "deployable_services"
    __table_args__ = (
        UniqueConstraint("organization_id", "slug", name="uq_service_slug"),
    )

    organization_id: Mapped[str] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        index=True,
    )
    team_id: Mapped[str | None] = mapped_column(
        ForeignKey("teams.id", ondelete="SET NULL"),
        index=True,
    )
    name: Mapped[str] = mapped_column(String(180), index=True)
    slug: Mapped[str] = mapped_column(String(180), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    repository_url: Mapped[str] = mapped_column(String(600))
    service_type: Mapped[ServiceType] = mapped_column(
        Enum(ServiceType, values_callable=enum_values, native_enum=False),
        nullable=False,
        index=True,
    )
    framework: Mapped[ServiceFramework] = mapped_column(
        Enum(ServiceFramework, values_callable=enum_values, native_enum=False),
        nullable=False,
        index=True,
    )
    status: Mapped[ServiceStatus] = mapped_column(
        Enum(ServiceStatus, values_callable=enum_values, native_enum=False),
        default=ServiceStatus.UNKNOWN,
        nullable=False,
        index=True,
    )
    owner_team: Mapped[str | None] = mapped_column(String(180), index=True)
    created_by: Mapped[str | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        index=True,
    )

    environments = relationship(
        "Environment",
        back_populates="service",
        cascade="all, delete-orphan",
    )


class Environment(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "service_environments"
    __table_args__ = (
        UniqueConstraint("service_id", "name", name="uq_service_environment_name"),
    )

    service_id: Mapped[str] = mapped_column(
        ForeignKey("deployable_services.id", ondelete="CASCADE"),
        index=True,
    )
    name: Mapped[EnvironmentName] = mapped_column(
        Enum(EnvironmentName, values_callable=enum_values, native_enum=False),
        nullable=False,
        index=True,
    )
    branch: Mapped[str] = mapped_column(String(180), default="main", nullable=False)
    base_url: Mapped[str | None] = mapped_column(String(600))
    status: Mapped[ServiceStatus] = mapped_column(
        Enum(ServiceStatus, values_callable=enum_values, native_enum=False),
        default=ServiceStatus.UNKNOWN,
        nullable=False,
        index=True,
    )
    auto_deploy_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    service = relationship("DeployableService", back_populates="environments")


class Deployment(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "deployments"

    service_id: Mapped[str] = mapped_column(
        ForeignKey("deployable_services.id", ondelete="CASCADE"),
        index=True,
    )
    environment_id: Mapped[str] = mapped_column(
        ForeignKey("service_environments.id", ondelete="CASCADE"),
        index=True,
    )
    version: Mapped[str] = mapped_column(String(80), index=True)
    commit_sha: Mapped[str] = mapped_column(String(64), index=True)
    branch: Mapped[str] = mapped_column(String(180), index=True)
    status: Mapped[DeploymentStatus] = mapped_column(
        Enum(DeploymentStatus, values_callable=enum_values, native_enum=False),
        default=DeploymentStatus.QUEUED,
        nullable=False,
        index=True,
    )
    triggered_by: Mapped[str | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"),
        index=True,
    )
    started_at: Mapped[datetime | None]
    finished_at: Mapped[datetime | None]
    duration_seconds: Mapped[int | None] = mapped_column(Integer)
    error_message: Mapped[str | None] = mapped_column(Text)
    rollback_source_deployment_id: Mapped[str | None] = mapped_column(
        ForeignKey("deployments.id", ondelete="SET NULL"),
        index=True,
    )


class DeploymentLog(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "deployment_logs"

    deployment_id: Mapped[str] = mapped_column(
        ForeignKey("deployments.id", ondelete="CASCADE"),
        index=True,
    )
    level: Mapped[LogLevel] = mapped_column(
        Enum(LogLevel, values_callable=enum_values, native_enum=False),
        default=LogLevel.INFO,
        nullable=False,
        index=True,
    )
    step: Mapped[str | None] = mapped_column(String(120))
    message: Mapped[str] = mapped_column(Text)


class EnvironmentVariable(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "environment_variables"
    __table_args__ = (
        UniqueConstraint("environment_id", "key", name="uq_environment_variable_key"),
    )

    environment_id: Mapped[str] = mapped_column(
        ForeignKey("service_environments.id", ondelete="CASCADE"),
        index=True,
    )
    key: Mapped[str] = mapped_column(String(180), index=True)
    value_masked: Mapped[str] = mapped_column(Text)
    is_secret: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)


class HealthCheck(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "health_checks"

    environment_id: Mapped[str] = mapped_column(
        ForeignKey("service_environments.id", ondelete="CASCADE"),
        index=True,
    )
    status: Mapped[ServiceStatus] = mapped_column(
        Enum(ServiceStatus, values_callable=enum_values, native_enum=False),
        default=ServiceStatus.UNKNOWN,
        nullable=False,
        index=True,
    )
    latency_ms: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    message: Mapped[str] = mapped_column(String(500), default="Health check pending.")
