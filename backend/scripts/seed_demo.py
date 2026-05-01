import asyncio

from app.core.security import hash_password
from app.db.session import AsyncSessionLocal
from app.models.audit_log import AuditLog
from app.models.enums import (
    DeploymentStatus,
    EnvironmentName,
    IncidentSeverity,
    IncidentStatus,
    LogLevel,
    ServiceFramework,
    ServiceStatus,
    ServiceType,
    UserRole,
    WorkspaceRole,
)
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
from app.models.user import User
from app.models.workspace import Organization, Workspace, WorkspaceMember


async def seed() -> None:
    async with AsyncSessionLocal() as session:
        user = User(
            email="platform@example.com",
            full_name="Platform Owner",
            hashed_password=hash_password("SecurePass123!"),
            role=UserRole.PLATFORM_OWNER,
        )
        session.add(user)
        await session.flush()

        organization = Organization(name="SpyloDEV Platform", slug="spylodev-platform")
        session.add(organization)
        await session.flush()

        workspace = Workspace(
            organization_id=organization.id,
            name="Deployment Platform",
            slug="deployment-platform",
        )
        session.add(workspace)
        await session.flush()
        session.add(
            WorkspaceMember(
                workspace_id=workspace.id,
                user_id=user.id,
                role=WorkspaceRole.PLATFORM_OWNER,
            )
        )

        team = Team(
            organization_id=organization.id, name="Core Platform", slug="core-platform"
        )
        session.add(team)
        await session.flush()

        service = DeployableService(
            organization_id=organization.id,
            team_id=team.id,
            name="customer-api",
            slug="customer-api",
            description="Customer-facing FastAPI backend.",
            repository_url="https://github.com/acme/customer-api",
            service_type=ServiceType.BACKEND,
            framework=ServiceFramework.FASTAPI,
            status=ServiceStatus.HEALTHY,
            owner_team="Core Platform",
            created_by=user.id,
        )
        session.add(service)
        await session.flush()

        staging = Environment(
            service_id=service.id,
            name=EnvironmentName.STAGING,
            branch="release",
            base_url="https://staging.customer-api.internal",
            status=ServiceStatus.HEALTHY,
            auto_deploy_enabled=True,
        )
        production = Environment(
            service_id=service.id,
            name=EnvironmentName.PRODUCTION,
            branch="main",
            base_url="https://api.customer-api.internal",
            status=ServiceStatus.HEALTHY,
            auto_deploy_enabled=False,
        )
        session.add_all([staging, production])
        await session.flush()

        deployment = Deployment(
            service_id=service.id,
            environment_id=production.id,
            version="v2.8.4",
            commit_sha="abc123456789",
            branch="main",
            status=DeploymentStatus.SUCCEEDED,
            triggered_by=user.id,
            duration_seconds=192,
        )
        session.add(deployment)
        await session.flush()

        for step in ["clone", "install", "test", "image", "release", "health"]:
            session.add(
                DeploymentLog(
                    deployment_id=deployment.id,
                    level=LogLevel.INFO,
                    step=step,
                    message=f"{step} completed",
                )
            )

        session.add_all(
            [
                EnvironmentVariable(
                    environment_id=production.id,
                    key="DATABASE_URL",
                    value_masked="********",
                    is_secret=True,
                ),
                HealthCheck(
                    environment_id=production.id,
                    status=ServiceStatus.HEALTHY,
                    latency_ms=83,
                    message="Production health check passed.",
                ),
            ]
        )

        incident = Incident(
            organization_id=organization.id,
            service_id=service.id,
            environment_id=production.id,
            title="production deployment latency spike",
            severity=IncidentSeverity.MEDIUM,
            status=IncidentStatus.INVESTIGATING,
        )
        session.add(incident)
        await session.flush()
        session.add(
            IncidentTimelineEntry(
                incident_id=incident.id,
                actor_id=user.id,
                message="Investigation started from failed health check alert.",
            )
        )

        for action, target_type, target_id in [
            ("user_registered", "user", user.id),
            ("workspace_created", "organization", organization.id),
            ("service_created", "service", service.id),
            ("deployment_succeeded", "deployment", deployment.id),
            ("env_var_created", "environment_variable", production.id),
        ]:
            session.add(
                AuditLog(
                    organization_id=organization.id,
                    workspace_id=workspace.id,
                    actor_id=user.id,
                    action=action,
                    target_type=target_type,
                    target_id=target_id,
                    metadata_json={},
                )
            )

        await session.commit()
        print("Seeded demo account platform@example.com / SecurePass123!")


if __name__ == "__main__":
    asyncio.run(seed())
