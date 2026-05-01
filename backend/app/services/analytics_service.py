from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.deployment import DeploymentRepository
from app.services.permissions import PermissionService


class AnalyticsService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = DeploymentRepository(session)
        self.permissions = PermissionService(session)

    async def overview(self, *, user_id: str, organization_id: str) -> dict:
        await self.permissions.require_role(
            organization_id=organization_id, user_id=user_id
        )
        return await self.repository.analytics_overview(
            user_id=user_id, organization_id=organization_id
        )

    async def deployments(self, *, user_id: str, organization_id: str) -> dict:
        await self.permissions.require_role(
            organization_id=organization_id, user_id=user_id
        )
        return {
            "deployments_per_day": await self.repository.deployments_per_day(
                user_id=user_id, organization_id=organization_id
            ),
            "most_deployed_service": None,
        }

    async def reliability(self, *, user_id: str, organization_id: str) -> dict:
        await self.permissions.require_role(
            organization_id=organization_id, user_id=user_id
        )
        return {"failure_rate_by_service": []}
