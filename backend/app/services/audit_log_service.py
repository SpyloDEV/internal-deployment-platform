from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import PermissionDeniedError
from app.models.audit_log import AuditLog
from app.repositories.deployment import DeploymentRepository


class AuditLogService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = DeploymentRepository(session)

    async def record(
        self,
        *,
        action: str,
        organization_id: str | None = None,
        workspace_id: str | None = None,
        actor_id: str | None = None,
        target_type: str | None = None,
        target_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> AuditLog:
        return await self.repository.create_audit_log(
            data={
                "organization_id": organization_id,
                "workspace_id": workspace_id,
                "actor_id": actor_id,
                "action": action,
                "target_type": target_type,
                "target_id": target_id,
                "metadata_json": metadata or {},
            }
        )

    async def list_logs(
        self, *, user_id: str, organization_id: str | None
    ) -> list[AuditLog]:
        if organization_id is not None:
            role = await self.repository.organization_role(
                organization_id=organization_id, user_id=user_id
            )
            if role is None:
                raise PermissionDeniedError(
                    "You do not have access to this organization."
                )
        return await self.repository.list_audit_logs(
            user_id=user_id, organization_id=organization_id
        )
