from sqlalchemy.ext.asyncio import AsyncSession

from app.models.service import HealthCheck
from app.repositories.deployment import DeploymentRepository
from app.services.audit_log_service import AuditLogService
from app.services.environment_service import EnvironmentService
from app.services.service_registry_service import ServiceRegistryService


class HealthService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = DeploymentRepository(session)
        self.environments = EnvironmentService(session)
        self.services = ServiceRegistryService(session)
        self.audit_logs = AuditLogService(session)

    async def run_check(
        self, *, environment_id: str, user_id: str, data: dict
    ) -> HealthCheck:
        environment = await self.environments.get(
            environment_id=environment_id, user_id=user_id
        )
        service = await self.services.get(
            service_id=environment.service_id, user_id=user_id
        )
        check = await self.repository.create_health_check(
            data={"environment_id": environment.id, **data}
        )
        environment.status = check.status
        service.status = check.status
        await self.audit_logs.record(
            action="health_check_ran",
            organization_id=service.organization_id,
            actor_id=user_id,
            target_type="health_check",
            target_id=check.id,
        )
        return check

    async def latest(self, *, environment_id: str, user_id: str) -> HealthCheck | None:
        await self.environments.get(environment_id=environment_id, user_id=user_id)
        checks = await self.repository.list_health_checks(environment_id=environment_id)
        return checks[0] if checks else None

    async def history(self, *, environment_id: str, user_id: str) -> list[HealthCheck]:
        await self.environments.get(environment_id=environment_id, user_id=user_id)
        return await self.repository.list_health_checks(environment_id=environment_id)
