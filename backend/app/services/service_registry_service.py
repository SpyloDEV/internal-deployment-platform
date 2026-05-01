from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.service import DeployableService
from app.repositories.deployment import DeploymentRepository
from app.services.audit_log_service import AuditLogService
from app.services.permissions import MANAGE_ROLES, PermissionService, slugify


class ServiceRegistryService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = DeploymentRepository(session)
        self.permissions = PermissionService(session)
        self.audit_logs = AuditLogService(session)

    async def create(self, *, user_id: str, data: dict) -> DeployableService:
        await self.permissions.require_role(
            organization_id=data["organization_id"],
            user_id=user_id,
            allowed_roles=MANAGE_ROLES,
        )
        service = await self.repository.create_service(
            data={
                **data,
                "repository_url": str(data["repository_url"]),
                "slug": slugify(data["name"], "service"),
                "created_by": user_id,
            }
        )
        await self.audit_logs.record(
            action="service_created",
            organization_id=service.organization_id,
            actor_id=user_id,
            target_type="service",
            target_id=service.id,
        )
        return service

    async def list(
        self, *, user_id: str, organization_id: str | None
    ) -> list[DeployableService]:
        return await self.repository.list_services(
            user_id=user_id, organization_id=organization_id
        )

    async def get(self, *, service_id: str, user_id: str) -> DeployableService:
        service = await self.repository.get_service_for_user(
            service_id=service_id, user_id=user_id
        )
        if service is None:
            raise NotFoundError("Service not found.")
        return service

    async def update(
        self, *, service_id: str, user_id: str, data: dict
    ) -> DeployableService:
        service = await self.get(service_id=service_id, user_id=user_id)
        await self.permissions.require_role(
            organization_id=service.organization_id,
            user_id=user_id,
            allowed_roles=MANAGE_ROLES,
        )
        if "repository_url" in data:
            data["repository_url"] = str(data["repository_url"])
        if "name" in data:
            service.slug = slugify(data["name"], "service")
        for field, value in data.items():
            setattr(service, field, value)
        await self.audit_logs.record(
            action="service_updated",
            organization_id=service.organization_id,
            actor_id=user_id,
            target_type="service",
            target_id=service.id,
        )
        return service

    async def delete(self, *, service_id: str, user_id: str) -> DeployableService:
        service = await self.get(service_id=service_id, user_id=user_id)
        await self.permissions.require_role(
            organization_id=service.organization_id,
            user_id=user_id,
            allowed_roles=MANAGE_ROLES,
        )
        return service
