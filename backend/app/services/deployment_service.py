from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError, ValidationAppError
from app.models.enums import DeploymentStatus, EnvironmentName, LogLevel, ServiceStatus
from app.models.service import Deployment, DeploymentLog
from app.repositories.deployment import DeploymentRepository
from app.services.audit_log_service import AuditLogService
from app.services.environment_service import EnvironmentService
from app.services.incident_service import IncidentService
from app.services.permissions import DEPLOY_ROLES, PermissionService
from app.services.policy_service import PolicyService
from app.services.service_registry_service import ServiceRegistryService


class DeploymentService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = DeploymentRepository(session)
        self.environments = EnvironmentService(session)
        self.services = ServiceRegistryService(session)
        self.policies = PolicyService(session)
        self.permissions = PermissionService(session)
        self.audit_logs = AuditLogService(session)
        self.incidents = IncidentService(session)

    async def trigger(
        self, *, environment_id: str, user_id: str, data: dict
    ) -> Deployment:
        environment = await self.environments.get(
            environment_id=environment_id, user_id=user_id
        )
        service = await self.services.get(
            service_id=environment.service_id, user_id=user_id
        )
        await self.permissions.require_role(
            organization_id=service.organization_id,
            user_id=user_id,
            allowed_roles=DEPLOY_ROLES,
        )
        evaluation = await self.policies.evaluate_deployment(
            service=service, environment=environment, user_id=user_id
        )
        if evaluation["status"] == "blocked":
            await self.audit_logs.record(
                action="policy_violation_created",
                organization_id=service.organization_id,
                actor_id=user_id,
                target_type="environment",
                target_id=environment.id,
                metadata=evaluation,
            )
            raise ValidationAppError(
                "Deployment blocked by policy guardrails.", extra=evaluation
            )
        now = datetime.now(UTC)
        deployment = await self.repository.create_deployment(
            data={
                "service_id": service.id,
                "environment_id": environment.id,
                "version": data.get("version") or f"release-{now:%Y%m%d%H%M%S}",
                "commit_sha": data["commit_sha"],
                "branch": data.get("branch") or environment.branch,
                "status": DeploymentStatus.QUEUED,
                "triggered_by": user_id,
                "started_at": now,
            }
        )
        await self.audit_logs.record(
            action="deployment_triggered",
            organization_id=service.organization_id,
            actor_id=user_id,
            target_type="deployment",
            target_id=deployment.id,
        )
        await self._simulate_deployment(
            deployment=deployment,
            force_failure=data.get("force_failure", False),
            organization_id=service.organization_id,
            environment_name=environment.name,
            user_id=user_id,
        )
        environment.status = (
            ServiceStatus.DEGRADED
            if deployment.status == DeploymentStatus.FAILED
            else ServiceStatus.HEALTHY
        )
        service.status = environment.status
        return deployment

    async def _simulate_deployment(
        self,
        *,
        deployment: Deployment,
        force_failure: bool,
        organization_id: str,
        environment_name: EnvironmentName,
        user_id: str,
    ) -> None:
        for step, message in [
            ("queued", "Deployment queued by platform API."),
            ("clone", "Cloning repository"),
            ("install", "Installing dependencies"),
            ("test", "Running test suite"),
            ("image", "Building deployment image"),
            ("release", "Deploying release to environment"),
            ("health", "Running health check"),
        ]:
            await self.repository.create_deployment_log(
                data={
                    "deployment_id": deployment.id,
                    "level": LogLevel.INFO,
                    "step": step,
                    "message": message,
                }
            )
            if step == "clone":
                deployment.status = DeploymentStatus.BUILDING
            if step == "release":
                deployment.status = DeploymentStatus.DEPLOYING
        deployment.finished_at = datetime.now(UTC)
        deployment.duration_seconds = 42
        if force_failure:
            deployment.status = DeploymentStatus.FAILED
            deployment.error_message = "Mock build failed during integration tests."
            await self.repository.create_deployment_log(
                data={
                    "deployment_id": deployment.id,
                    "level": LogLevel.ERROR,
                    "step": "test",
                    "message": deployment.error_message,
                }
            )
            await self.audit_logs.record(
                action="deployment_failed",
                organization_id=organization_id,
                actor_id=user_id,
                target_type="deployment",
                target_id=deployment.id,
            )
            if environment_name == EnvironmentName.PRODUCTION:
                await self.incidents.create(
                    user_id=user_id,
                    data={
                        "organization_id": organization_id,
                        "service_id": deployment.service_id,
                        "environment_id": deployment.environment_id,
                        "deployment_id": deployment.id,
                        "title": "Failed production deployment",
                        "severity": "high",
                    },
                )
        else:
            deployment.status = DeploymentStatus.SUCCEEDED
            await self.repository.create_deployment_log(
                data={
                    "deployment_id": deployment.id,
                    "level": LogLevel.INFO,
                    "step": "complete",
                    "message": "Deployment succeeded",
                }
            )
            await self.audit_logs.record(
                action="deployment_succeeded",
                organization_id=organization_id,
                actor_id=user_id,
                target_type="deployment",
                target_id=deployment.id,
            )

    async def list(
        self,
        *,
        user_id: str,
        service_id: str | None = None,
        environment_id: str | None = None,
    ) -> list[Deployment]:
        return await self.repository.list_deployments(
            user_id=user_id, service_id=service_id, environment_id=environment_id
        )

    async def get(self, *, deployment_id: str, user_id: str) -> Deployment:
        deployment = await self.repository.get_deployment_for_user(
            deployment_id=deployment_id, user_id=user_id
        )
        if deployment is None:
            raise NotFoundError("Deployment not found.")
        return deployment

    async def cancel(self, *, deployment_id: str, user_id: str) -> Deployment:
        deployment = await self.get(deployment_id=deployment_id, user_id=user_id)
        if deployment.status in {
            DeploymentStatus.QUEUED,
            DeploymentStatus.BUILDING,
            DeploymentStatus.DEPLOYING,
        }:
            deployment.status = DeploymentStatus.CANCELLED
            deployment.finished_at = datetime.now(UTC)
        return deployment

    async def rollback(self, *, deployment_id: str, user_id: str) -> Deployment:
        source = await self.get(deployment_id=deployment_id, user_id=user_id)
        if source.status != DeploymentStatus.SUCCEEDED:
            raise ValidationAppError(
                "Only successful deployments can be rollback targets."
            )
        deployment = await self.repository.create_deployment(
            data={
                "service_id": source.service_id,
                "environment_id": source.environment_id,
                "version": f"rollback-{source.version}",
                "commit_sha": source.commit_sha,
                "branch": source.branch,
                "status": DeploymentStatus.ROLLED_BACK,
                "triggered_by": user_id,
                "started_at": datetime.now(UTC),
                "finished_at": datetime.now(UTC),
                "duration_seconds": 18,
                "rollback_source_deployment_id": source.id,
            }
        )
        await self.repository.create_deployment_log(
            data={
                "deployment_id": deployment.id,
                "level": LogLevel.INFO,
                "step": "rollback",
                "message": f"Rolled back to deployment {source.id}.",
            }
        )
        service = await self.services.get(service_id=source.service_id, user_id=user_id)
        await self.audit_logs.record(
            action="rollback_triggered",
            organization_id=service.organization_id,
            actor_id=user_id,
            target_type="deployment",
            target_id=deployment.id,
            metadata={"source_deployment_id": source.id},
        )
        return deployment

    async def logs(self, *, deployment_id: str, user_id: str) -> list[DeploymentLog]:
        await self.get(deployment_id=deployment_id, user_id=user_id)
        return await self.repository.list_deployment_logs(deployment_id=deployment_id)
