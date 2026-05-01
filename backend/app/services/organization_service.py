from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import ConflictError, NotFoundError
from app.models.enums import WorkspaceRole
from app.models.workspace import Organization
from app.repositories.deployment import DeploymentRepository
from app.services.audit_log_service import AuditLogService
from app.services.permissions import MANAGE_ROLES, PermissionService, slugify


class OrganizationService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = DeploymentRepository(session)
        self.permissions = PermissionService(session)
        self.audit_logs = AuditLogService(session)

    async def create(
        self, *, user_id: str, name: str, slug: str | None
    ) -> Organization:
        organization_slug = slugify(slug or name, "organization")
        if await self.repository.get_organization_by_slug(organization_slug):
            raise ConflictError("An organization with this slug already exists.")
        organization = await self.repository.create_organization(
            name=name, slug=organization_slug
        )
        workspace = await self.repository.create_workspace(
            organization_id=organization.id,
            name=f"{name} Platform",
            slug=f"{organization_slug}-platform",
        )
        await self.repository.add_member(
            workspace_id=workspace.id,
            user_id=user_id,
            role=WorkspaceRole.PLATFORM_OWNER,
        )
        await self.audit_logs.record(
            action="workspace_created",
            organization_id=organization.id,
            workspace_id=workspace.id,
            actor_id=user_id,
            target_type="organization",
            target_id=organization.id,
        )
        return organization

    async def list(self, *, user_id: str) -> list[Organization]:
        return await self.repository.list_organizations_for_user(user_id=user_id)

    async def get(self, *, organization_id: str, user_id: str) -> Organization:
        organization = await self.repository.get_organization(organization_id)
        if organization is None:
            raise NotFoundError("Organization not found.")
        await self.permissions.require_role(
            organization_id=organization_id, user_id=user_id
        )
        return organization

    async def update(
        self, *, organization_id: str, user_id: str, data: dict
    ) -> Organization:
        organization = await self.get(organization_id=organization_id, user_id=user_id)
        await self.permissions.require_role(
            organization_id=organization_id,
            user_id=user_id,
            allowed_roles=MANAGE_ROLES,
        )
        if "name" in data:
            organization.name = data["name"]
        return organization
