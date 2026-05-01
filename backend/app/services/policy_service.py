from sqlalchemy.ext.asyncio import AsyncSession

from app.models.enums import EnvironmentName, ServiceStatus, WorkspaceRole
from app.models.service import DeployableService, Environment
from app.repositories.deployment import DeploymentRepository


class PolicyService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = DeploymentRepository(session)

    async def evaluate_deployment(
        self, *, service: DeployableService, environment: Environment, user_id: str
    ) -> dict:
        role = await self.repository.organization_role(
            organization_id=service.organization_id, user_id=user_id
        )
        violations = []
        if environment.name == EnvironmentName.PRODUCTION and role not in {
            WorkspaceRole.PLATFORM_OWNER,
            WorkspaceRole.ADMIN,
            WorkspaceRole.OWNER,
        }:
            violations.append(
                {
                    "code": "production_admin_required",
                    "severity": "blocker",
                    "message": "Production deployments require platform_owner or admin.",
                    "blocking": True,
                }
            )
        if environment.name == EnvironmentName.PRODUCTION:
            has_staging = await self.repository.successful_staging_deployment_exists(
                service_id=service.id
            )
            if not has_staging:
                violations.append(
                    {
                        "code": "staging_success_required",
                        "severity": "blocker",
                        "message": "Production deploys require a successful staging deployment first.",
                        "blocking": True,
                    }
                )
        if not service.owner_team:
            violations.append(
                {
                    "code": "owner_team_required",
                    "severity": "blocker",
                    "message": "Service must have an owner_team before deployment.",
                    "blocking": True,
                }
            )
        if service.status == ServiceStatus.OFFLINE:
            violations.append(
                {
                    "code": "offline_service_blocked",
                    "severity": "blocker",
                    "message": "Deployment is blocked while the service is offline.",
                    "blocking": True,
                }
            )
        if environment.name == EnvironmentName.PRODUCTION:
            violations.append(
                {
                    "code": "production_env_var_audit",
                    "severity": "warning",
                    "message": "Production environment changes are audited and reviewed.",
                    "blocking": False,
                }
            )
        return {
            "status": (
                "blocked" if any(item["blocking"] for item in violations) else "passed"
            ),
            "violations": violations,
        }

    def policy_catalog(self) -> list[dict[str, str]]:
        return [
            {"code": "production_admin_required", "name": "Production admin required"},
            {"code": "staging_success_required", "name": "Staging success required"},
            {"code": "owner_team_required", "name": "Service owner team required"},
            {"code": "offline_service_blocked", "name": "Offline service blocked"},
            {"code": "production_env_var_audit", "name": "Production secret audit"},
        ]
