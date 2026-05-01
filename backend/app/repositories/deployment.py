from datetime import UTC, datetime, timedelta
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.audit_log import AuditLog
from app.models.enums import DeploymentStatus, EnvironmentName
from app.models.incident import Incident, IncidentTimelineEntry
from app.models.service import (
    DeployableService,
    Deployment,
    DeploymentLog,
    Environment,
    EnvironmentVariable,
    HealthCheck,
    Team,
)
from app.models.workspace import Organization, Workspace, WorkspaceMember


class DeploymentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_organization(self, organization_id: str) -> Organization | None:
        return await self.session.get(Organization, organization_id)

    async def get_organization_by_slug(self, slug: str) -> Organization | None:
        result = await self.session.execute(
            select(Organization).where(Organization.slug == slug)
        )
        return result.scalar_one_or_none()

    async def create_organization(self, *, name: str, slug: str) -> Organization:
        organization = Organization(name=name, slug=slug)
        self.session.add(organization)
        await self.session.flush()
        return organization

    async def create_workspace(
        self, *, organization_id: str, name: str, slug: str
    ) -> Workspace:
        workspace = Workspace(organization_id=organization_id, name=name, slug=slug)
        self.session.add(workspace)
        await self.session.flush()
        return workspace

    async def add_member(self, *, workspace_id: str, user_id: str, role: Any) -> None:
        self.session.add(
            WorkspaceMember(workspace_id=workspace_id, user_id=user_id, role=role)
        )
        await self.session.flush()

    async def organization_role(self, *, organization_id: str, user_id: str) -> Any:
        result = await self.session.execute(
            select(WorkspaceMember.role)
            .join(Workspace, Workspace.id == WorkspaceMember.workspace_id)
            .where(
                Workspace.organization_id == organization_id,
                WorkspaceMember.user_id == user_id,
            )
            .limit(1)
        )
        return result.scalar_one_or_none()

    async def list_organizations_for_user(self, *, user_id: str) -> list[Organization]:
        result = await self.session.execute(
            select(Organization)
            .join(Workspace, Workspace.organization_id == Organization.id)
            .join(WorkspaceMember, WorkspaceMember.workspace_id == Workspace.id)
            .where(WorkspaceMember.user_id == user_id)
            .order_by(Organization.created_at.desc())
        )
        return list(result.scalars().unique().all())

    async def create_team(self, *, data: dict[str, Any]) -> Team:
        team = Team(**data)
        self.session.add(team)
        await self.session.flush()
        return team

    async def list_teams(self, *, organization_id: str) -> list[Team]:
        result = await self.session.execute(
            select(Team)
            .where(Team.organization_id == organization_id)
            .order_by(Team.created_at.desc())
        )
        return list(result.scalars().all())

    async def get_team(self, team_id: str) -> Team | None:
        return await self.session.get(Team, team_id)

    async def create_service(self, *, data: dict[str, Any]) -> DeployableService:
        service = DeployableService(**data)
        self.session.add(service)
        await self.session.flush()
        return service

    async def list_services(
        self, *, organization_id: str | None, user_id: str
    ) -> list[DeployableService]:
        filters = [WorkspaceMember.user_id == user_id]
        if organization_id:
            filters.append(DeployableService.organization_id == organization_id)
        result = await self.session.execute(
            select(DeployableService)
            .join(
                Workspace,
                Workspace.organization_id == DeployableService.organization_id,
            )
            .join(WorkspaceMember, WorkspaceMember.workspace_id == Workspace.id)
            .where(*filters)
            .order_by(DeployableService.created_at.desc())
        )
        return list(result.scalars().unique().all())

    async def get_service_for_user(
        self, *, service_id: str, user_id: str
    ) -> DeployableService | None:
        result = await self.session.execute(
            select(DeployableService)
            .join(
                Workspace,
                Workspace.organization_id == DeployableService.organization_id,
            )
            .join(WorkspaceMember, WorkspaceMember.workspace_id == Workspace.id)
            .where(
                DeployableService.id == service_id, WorkspaceMember.user_id == user_id
            )
        )
        return result.scalar_one_or_none()

    async def create_environment(self, *, data: dict[str, Any]) -> Environment:
        environment = Environment(**data)
        self.session.add(environment)
        await self.session.flush()
        return environment

    async def list_environments(self, *, service_id: str) -> list[Environment]:
        result = await self.session.execute(
            select(Environment)
            .where(Environment.service_id == service_id)
            .order_by(Environment.created_at.asc())
        )
        return list(result.scalars().all())

    async def get_environment_for_user(
        self, *, environment_id: str, user_id: str
    ) -> Environment | None:
        result = await self.session.execute(
            select(Environment)
            .join(DeployableService, DeployableService.id == Environment.service_id)
            .join(
                Workspace,
                Workspace.organization_id == DeployableService.organization_id,
            )
            .join(WorkspaceMember, WorkspaceMember.workspace_id == Workspace.id)
            .where(Environment.id == environment_id, WorkspaceMember.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_deployment(self, *, data: dict[str, Any]) -> Deployment:
        deployment = Deployment(**data)
        self.session.add(deployment)
        await self.session.flush()
        return deployment

    async def get_deployment_for_user(
        self, *, deployment_id: str, user_id: str
    ) -> Deployment | None:
        result = await self.session.execute(
            select(Deployment)
            .join(Environment, Environment.id == Deployment.environment_id)
            .join(DeployableService, DeployableService.id == Deployment.service_id)
            .join(
                Workspace,
                Workspace.organization_id == DeployableService.organization_id,
            )
            .join(WorkspaceMember, WorkspaceMember.workspace_id == Workspace.id)
            .where(Deployment.id == deployment_id, WorkspaceMember.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def list_deployments(
        self,
        *,
        user_id: str,
        service_id: str | None = None,
        environment_id: str | None = None,
    ) -> list[Deployment]:
        filters = [WorkspaceMember.user_id == user_id]
        if service_id:
            filters.append(Deployment.service_id == service_id)
        if environment_id:
            filters.append(Deployment.environment_id == environment_id)
        result = await self.session.execute(
            select(Deployment)
            .join(Environment, Environment.id == Deployment.environment_id)
            .join(DeployableService, DeployableService.id == Deployment.service_id)
            .join(
                Workspace,
                Workspace.organization_id == DeployableService.organization_id,
            )
            .join(WorkspaceMember, WorkspaceMember.workspace_id == Workspace.id)
            .where(*filters)
            .order_by(Deployment.created_at.desc())
            .limit(100)
        )
        return list(result.scalars().unique().all())

    async def create_deployment_log(self, *, data: dict[str, Any]) -> DeploymentLog:
        log = DeploymentLog(**data)
        self.session.add(log)
        await self.session.flush()
        return log

    async def list_deployment_logs(self, *, deployment_id: str) -> list[DeploymentLog]:
        result = await self.session.execute(
            select(DeploymentLog)
            .where(DeploymentLog.deployment_id == deployment_id)
            .order_by(DeploymentLog.created_at.asc())
        )
        return list(result.scalars().all())

    async def successful_staging_deployment_exists(self, *, service_id: str) -> bool:
        result = await self.session.execute(
            select(Deployment.id)
            .join(Environment, Environment.id == Deployment.environment_id)
            .where(
                Deployment.service_id == service_id,
                Deployment.status == DeploymentStatus.SUCCEEDED,
                Environment.name == EnvironmentName.STAGING,
            )
            .limit(1)
        )
        return result.scalar_one_or_none() is not None

    async def create_env_var(self, *, data: dict[str, Any]) -> EnvironmentVariable:
        env_var = EnvironmentVariable(**data)
        self.session.add(env_var)
        await self.session.flush()
        return env_var

    async def get_env_var_for_user(
        self, *, env_var_id: str, user_id: str
    ) -> EnvironmentVariable | None:
        result = await self.session.execute(
            select(EnvironmentVariable)
            .join(Environment, Environment.id == EnvironmentVariable.environment_id)
            .join(DeployableService, DeployableService.id == Environment.service_id)
            .join(
                Workspace,
                Workspace.organization_id == DeployableService.organization_id,
            )
            .join(WorkspaceMember, WorkspaceMember.workspace_id == Workspace.id)
            .where(
                EnvironmentVariable.id == env_var_id,
                WorkspaceMember.user_id == user_id,
            )
        )
        return result.scalar_one_or_none()

    async def list_env_vars(self, *, environment_id: str) -> list[EnvironmentVariable]:
        result = await self.session.execute(
            select(EnvironmentVariable)
            .where(EnvironmentVariable.environment_id == environment_id)
            .order_by(EnvironmentVariable.key.asc())
        )
        return list(result.scalars().all())

    async def create_health_check(self, *, data: dict[str, Any]) -> HealthCheck:
        check = HealthCheck(**data)
        self.session.add(check)
        await self.session.flush()
        return check

    async def list_health_checks(self, *, environment_id: str) -> list[HealthCheck]:
        result = await self.session.execute(
            select(HealthCheck)
            .where(HealthCheck.environment_id == environment_id)
            .order_by(HealthCheck.created_at.desc())
            .limit(50)
        )
        return list(result.scalars().all())

    async def create_audit_log(self, *, data: dict[str, Any]) -> AuditLog:
        log = AuditLog(**data)
        self.session.add(log)
        await self.session.flush()
        return log

    async def list_audit_logs(
        self, *, user_id: str, organization_id: str | None
    ) -> list[AuditLog]:
        filters = [WorkspaceMember.user_id == user_id]
        if organization_id:
            filters.append(AuditLog.organization_id == organization_id)
        result = await self.session.execute(
            select(AuditLog)
            .join(Workspace, Workspace.organization_id == AuditLog.organization_id)
            .join(WorkspaceMember, WorkspaceMember.workspace_id == Workspace.id)
            .where(*filters)
            .order_by(AuditLog.created_at.desc())
            .limit(100)
        )
        return list(result.scalars().unique().all())

    async def create_incident(self, *, data: dict[str, Any]) -> Incident:
        incident = Incident(**data)
        self.session.add(incident)
        await self.session.flush()
        return incident

    async def get_incident_for_user(
        self, *, incident_id: str, user_id: str
    ) -> Incident | None:
        result = await self.session.execute(
            select(Incident)
            .join(Workspace, Workspace.organization_id == Incident.organization_id)
            .join(WorkspaceMember, WorkspaceMember.workspace_id == Workspace.id)
            .where(Incident.id == incident_id, WorkspaceMember.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def list_incidents(
        self, *, user_id: str, organization_id: str | None
    ) -> list[Incident]:
        filters = [WorkspaceMember.user_id == user_id]
        if organization_id:
            filters.append(Incident.organization_id == organization_id)
        result = await self.session.execute(
            select(Incident)
            .join(Workspace, Workspace.organization_id == Incident.organization_id)
            .join(WorkspaceMember, WorkspaceMember.workspace_id == Workspace.id)
            .where(*filters)
            .order_by(Incident.created_at.desc())
        )
        return list(result.scalars().unique().all())

    async def create_incident_timeline(
        self, *, data: dict[str, Any]
    ) -> IncidentTimelineEntry:
        entry = IncidentTimelineEntry(**data)
        self.session.add(entry)
        await self.session.flush()
        return entry

    async def analytics_overview(self, *, user_id: str, organization_id: str) -> dict:
        member_filter = [
            Workspace.organization_id == organization_id,
            WorkspaceMember.user_id == user_id,
        ]
        total_services = await self.session.scalar(
            select(func.count(DeployableService.id))
            .join(
                Workspace,
                Workspace.organization_id == DeployableService.organization_id,
            )
            .join(WorkspaceMember, WorkspaceMember.workspace_id == Workspace.id)
            .where(*member_filter)
        )
        total_environments = await self.session.scalar(
            select(func.count(Environment.id))
            .join(DeployableService, DeployableService.id == Environment.service_id)
            .join(
                Workspace,
                Workspace.organization_id == DeployableService.organization_id,
            )
            .join(WorkspaceMember, WorkspaceMember.workspace_id == Workspace.id)
            .where(*member_filter)
        )
        total_deployments = await self.session.scalar(
            select(func.count(Deployment.id))
            .join(Environment, Environment.id == Deployment.environment_id)
            .join(DeployableService, DeployableService.id == Deployment.service_id)
            .join(
                Workspace,
                Workspace.organization_id == DeployableService.organization_id,
            )
            .join(WorkspaceMember, WorkspaceMember.workspace_id == Workspace.id)
            .where(*member_filter)
        )
        successful = await self.session.scalar(
            select(func.count(Deployment.id))
            .join(Environment, Environment.id == Deployment.environment_id)
            .join(DeployableService, DeployableService.id == Deployment.service_id)
            .join(
                Workspace,
                Workspace.organization_id == DeployableService.organization_id,
            )
            .join(WorkspaceMember, WorkspaceMember.workspace_id == Workspace.id)
            .where(Deployment.status == DeploymentStatus.SUCCEEDED, *member_filter)
        )
        failed = await self.session.scalar(
            select(func.count(Deployment.id))
            .join(Environment, Environment.id == Deployment.environment_id)
            .join(DeployableService, DeployableService.id == Deployment.service_id)
            .join(
                Workspace,
                Workspace.organization_id == DeployableService.organization_id,
            )
            .join(WorkspaceMember, WorkspaceMember.workspace_id == Workspace.id)
            .where(Deployment.status == DeploymentStatus.FAILED, *member_filter)
        )
        rollbacks = await self.session.scalar(
            select(func.count(Deployment.id))
            .join(Environment, Environment.id == Deployment.environment_id)
            .join(DeployableService, DeployableService.id == Deployment.service_id)
            .join(
                Workspace,
                Workspace.organization_id == DeployableService.organization_id,
            )
            .join(WorkspaceMember, WorkspaceMember.workspace_id == Workspace.id)
            .where(Deployment.status == DeploymentStatus.ROLLED_BACK, *member_filter)
        )
        avg_duration = await self.session.scalar(
            select(func.avg(Deployment.duration_seconds))
            .join(Environment, Environment.id == Deployment.environment_id)
            .join(DeployableService, DeployableService.id == Deployment.service_id)
            .join(
                Workspace,
                Workspace.organization_id == DeployableService.organization_id,
            )
            .join(WorkspaceMember, WorkspaceMember.workspace_id == Workspace.id)
            .where(*member_filter)
        )
        total = int(total_deployments or 0)
        succeeded = int(successful or 0)
        return {
            "total_services": int(total_services or 0),
            "total_environments": int(total_environments or 0),
            "total_deployments": total,
            "successful_deployments": succeeded,
            "failed_deployments": int(failed or 0),
            "success_rate": round((succeeded / total) * 100, 2) if total else 0.0,
            "average_duration_seconds": (
                round(float(avg_duration), 2) if avg_duration is not None else None
            ),
            "rollback_count": int(rollbacks or 0),
        }

    async def deployments_per_day(
        self, *, user_id: str, organization_id: str, days: int = 7
    ) -> list[dict[str, int | str]]:
        since = datetime.now(UTC) - timedelta(days=days - 1)
        result = await self.session.execute(
            select(Deployment.created_at)
            .join(Environment, Environment.id == Deployment.environment_id)
            .join(DeployableService, DeployableService.id == Deployment.service_id)
            .join(
                Workspace,
                Workspace.organization_id == DeployableService.organization_id,
            )
            .join(WorkspaceMember, WorkspaceMember.workspace_id == Workspace.id)
            .where(
                Workspace.organization_id == organization_id,
                WorkspaceMember.user_id == user_id,
                Deployment.created_at >= since,
            )
        )
        counts: dict[str, int] = {}
        for (created_at,) in result.all():
            key = created_at.date().isoformat()
            counts[key] = counts.get(key, 0) + 1
        return [
            {
                "date": (since + timedelta(days=offset)).date().isoformat(),
                "deployments": counts.get(
                    (since + timedelta(days=offset)).date().isoformat(), 0
                ),
            }
            for offset in range(days)
        ]
