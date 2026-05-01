from datetime import datetime

from sqlalchemy import JSON, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import ApiKeyStatus, enum_values


class ApiKey(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "api_keys"

    workspace_id: Mapped[str] = mapped_column(
        ForeignKey("workspaces.id", ondelete="CASCADE"),
        index=True,
    )
    name: Mapped[str] = mapped_column(String(180))
    key_hash: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    key_prefix: Mapped[str] = mapped_column(String(16))
    scopes: Mapped[list] = mapped_column(JSON, default=list, nullable=False)
    requests_per_minute: Mapped[int] = mapped_column(
        Integer, default=60, nullable=False
    )
    status: Mapped[ApiKeyStatus] = mapped_column(
        Enum(ApiKeyStatus, values_callable=enum_values, native_enum=False),
        default=ApiKeyStatus.ACTIVE,
        nullable=False,
        index=True,
    )
    last_used_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
