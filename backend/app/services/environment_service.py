from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.service import Environment
from app.repositories.deployment import DeploymentRepository
from app.services.audit_log_service import AuditLogService
from app.services.permissions import MANAGE_ROLES, PermissionService
from app.services.service_registry_service import ServiceRegistryService


class EnvironmentService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = DeploymentRepository(session)
        self.services = ServiceRegistryService(session)
        self.permissions = PermissionService(session)
        self.audit_logs = AuditLogService(session)

    async def create(self, *, service_id: str, user_id: str, data: dict) -> Environment:
        service = await self.services.get(service_id=service_id, user_id=user_id)
        await self.permissions.require_role(
            organization_id=service.organization_id,
            user_id=user_id,
            allowed_roles=MANAGE_ROLES,
        )
        environment = await self.repository.create_environment(
            data={
                **data,
                "base_url": str(data["base_url"]) if data.get("base_url") else None,
                "service_id": service.id,
            }
        )
        await self.audit_logs.record(
            action="environment_created",
            organization_id=service.organization_id,
            actor_id=user_id,
            target_type="environment",
            target_id=environment.id,
        )
        return environment

    async def list(self, *, service_id: str, user_id: str) -> list[Environment]:
        await self.services.get(service_id=service_id, user_id=user_id)
        return await self.repository.list_environments(service_id=service_id)

    async def get(self, *, environment_id: str, user_id: str) -> Environment:
        environment = await self.repository.get_environment_for_user(
            environment_id=environment_id, user_id=user_id
        )
        if environment is None:
            raise NotFoundError("Environment not found.")
        return environment

    async def update(
        self, *, environment_id: str, user_id: str, data: dict
    ) -> Environment:
        environment = await self.get(environment_id=environment_id, user_id=user_id)
        service = await self.services.get(
            service_id=environment.service_id, user_id=user_id
        )
        await self.permissions.require_role(
            organization_id=service.organization_id,
            user_id=user_id,
            allowed_roles=MANAGE_ROLES,
        )
        if "base_url" in data:
            data["base_url"] = str(data["base_url"]) if data["base_url"] else None
        for field, value in data.items():
            setattr(environment, field, value)
        return environment
