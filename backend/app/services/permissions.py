import re

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import PermissionDeniedError
from app.models.enums import WorkspaceRole
from app.repositories.deployment import DeploymentRepository

MANAGE_ROLES = {WorkspaceRole.PLATFORM_OWNER, WorkspaceRole.ADMIN, WorkspaceRole.OWNER}
DEPLOY_ROLES = MANAGE_ROLES | {WorkspaceRole.DEVELOPER}


def slugify(value: str, fallback: str = "resource") -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or fallback


class PermissionService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = DeploymentRepository(session)

    async def require_role(
        self,
        *,
        organization_id: str,
        user_id: str,
        allowed_roles: set[WorkspaceRole] | None = None,
    ) -> WorkspaceRole:
        role = await self.repository.organization_role(
            organization_id=organization_id, user_id=user_id
        )
        if role is None:
            raise PermissionDeniedError("You do not have access to this organization.")
        if allowed_roles is not None and role not in allowed_roles:
            raise PermissionDeniedError(
                "Your role is not allowed to perform this action."
            )
        return role
