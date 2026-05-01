from sqlalchemy import Enum, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin
from app.models.enums import WorkspaceRole, enum_values


class Organization(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "organizations"

    name: Mapped[str] = mapped_column(String(180), index=True)
    slug: Mapped[str] = mapped_column(String(180), unique=True, index=True)

    workspaces = relationship("Workspace", back_populates="organization")


class Workspace(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "workspaces"

    organization_id: Mapped[str | None] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        index=True,
    )
    name: Mapped[str] = mapped_column(String(180), index=True)
    slug: Mapped[str] = mapped_column(String(180), unique=True, index=True)

    organization = relationship("Organization", back_populates="workspaces")
    members = relationship(
        "WorkspaceMember",
        back_populates="workspace",
        cascade="all, delete-orphan",
    )


class WorkspaceMember(UUIDPrimaryKeyMixin, TimestampMixin, Base):
    __tablename__ = "workspace_members"
    __table_args__ = (
        UniqueConstraint("workspace_id", "user_id", name="uq_workspace_member_user"),
    )

    workspace_id: Mapped[str] = mapped_column(
        ForeignKey("workspaces.id", ondelete="CASCADE"),
        index=True,
    )
    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    role: Mapped[WorkspaceRole] = mapped_column(
        Enum(WorkspaceRole, values_callable=enum_values, native_enum=False),
        default=WorkspaceRole.MEMBER,
        nullable=False,
        index=True,
    )

    workspace = relationship("Workspace", back_populates="members")
    user = relationship("User", back_populates="memberships")
