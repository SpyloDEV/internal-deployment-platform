from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.service import Team
from app.repositories.deployment import DeploymentRepository
from app.services.audit_log_service import AuditLogService
from app.services.permissions import MANAGE_ROLES, PermissionService, slugify


class TeamService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = DeploymentRepository(session)
        self.permissions = PermissionService(session)
        self.audit_logs = AuditLogService(session)

    async def create(self, *, user_id: str, data: dict) -> Team:
        await self.permissions.require_role(
            organization_id=data["organization_id"],
            user_id=user_id,
            allowed_roles=MANAGE_ROLES,
        )
        team = await self.repository.create_team(
            data={**data, "slug": slugify(data.get("slug") or data["name"], "team")}
        )
        await self.audit_logs.record(
            action="team_created",
            organization_id=team.organization_id,
            actor_id=user_id,
            target_type="team",
            target_id=team.id,
        )
        return team

    async def list(self, *, user_id: str, organization_id: str) -> list[Team]:
        await self.permissions.require_role(
            organization_id=organization_id, user_id=user_id
        )
        return await self.repository.list_teams(organization_id=organization_id)

    async def update(self, *, user_id: str, team_id: str, data: dict) -> Team:
        team = await self.repository.get_team(team_id)
        if team is None:
            raise NotFoundError("Team not found.")
        await self.permissions.require_role(
            organization_id=team.organization_id,
            user_id=user_id,
            allowed_roles=MANAGE_ROLES,
        )
        if "name" in data:
            team.name = data["name"]
            team.slug = slugify(data["name"], "team")
        return team
