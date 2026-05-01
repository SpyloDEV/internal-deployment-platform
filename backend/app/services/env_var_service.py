from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.service import EnvironmentVariable
from app.repositories.deployment import DeploymentRepository
from app.services.audit_log_service import AuditLogService
from app.services.environment_service import EnvironmentService
from app.services.permissions import MANAGE_ROLES, PermissionService
from app.services.service_registry_service import ServiceRegistryService


def _mask(value: str, is_secret: bool) -> str:
    return "********" if is_secret else value


class EnvVarService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = DeploymentRepository(session)
        self.environments = EnvironmentService(session)
        self.services = ServiceRegistryService(session)
        self.permissions = PermissionService(session)
        self.audit_logs = AuditLogService(session)

    async def create(
        self, *, environment_id: str, user_id: str, data: dict
    ) -> EnvironmentVariable:
        environment = await self.environments.get(
            environment_id=environment_id, user_id=user_id
        )
        service = await self.services.get(
            service_id=environment.service_id, user_id=user_id
        )
        await self.permissions.require_role(
            organization_id=service.organization_id,
            user_id=user_id,
            allowed_roles=MANAGE_ROLES,
        )
        env_var = await self.repository.create_env_var(
            data={
                "environment_id": environment.id,
                "key": data["key"],
                "value_masked": _mask(data["value"], data["is_secret"]),
                "is_secret": data["is_secret"],
            }
        )
        await self.audit_logs.record(
            action="env_var_created",
            organization_id=service.organization_id,
            actor_id=user_id,
            target_type="environment_variable",
            target_id=env_var.id,
            metadata={"key": env_var.key, "is_secret": env_var.is_secret},
        )
        return env_var

    async def list(
        self, *, environment_id: str, user_id: str
    ) -> list[EnvironmentVariable]:
        await self.environments.get(environment_id=environment_id, user_id=user_id)
        return await self.repository.list_env_vars(environment_id=environment_id)

    async def update(
        self, *, env_var_id: str, user_id: str, data: dict
    ) -> EnvironmentVariable:
        env_var = await self.repository.get_env_var_for_user(
            env_var_id=env_var_id, user_id=user_id
        )
        if env_var is None:
            raise NotFoundError("Environment variable not found.")
        environment = await self.environments.get(
            environment_id=env_var.environment_id, user_id=user_id
        )
        service = await self.services.get(
            service_id=environment.service_id, user_id=user_id
        )
        await self.permissions.require_role(
            organization_id=service.organization_id,
            user_id=user_id,
            allowed_roles=MANAGE_ROLES,
        )
        is_secret = data.get("is_secret", env_var.is_secret)
        if "value" in data:
            env_var.value_masked = _mask(data["value"], is_secret)
        env_var.is_secret = is_secret
        await self.audit_logs.record(
            action="env_var_updated",
            organization_id=service.organization_id,
            actor_id=user_id,
            target_type="environment_variable",
            target_id=env_var.id,
        )
        return env_var

    async def delete(self, *, env_var_id: str, user_id: str) -> EnvironmentVariable:
        env_var = await self.repository.get_env_var_for_user(
            env_var_id=env_var_id, user_id=user_id
        )
        if env_var is None:
            raise NotFoundError("Environment variable not found.")
        environment = await self.environments.get(
            environment_id=env_var.environment_id, user_id=user_id
        )
        service = await self.services.get(
            service_id=environment.service_id, user_id=user_id
        )
        await self.audit_logs.record(
            action="env_var_deleted",
            organization_id=service.organization_id,
            actor_id=user_id,
            target_type="environment_variable",
            target_id=env_var.id,
        )
        return env_var
