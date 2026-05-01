from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.enums import IncidentStatus
from app.models.incident import Incident, IncidentTimelineEntry
from app.repositories.deployment import DeploymentRepository
from app.services.audit_log_service import AuditLogService
from app.services.permissions import PermissionService


class IncidentService:
    def __init__(self, session: AsyncSession) -> None:
        self.repository = DeploymentRepository(session)
        self.permissions = PermissionService(session)
        self.audit_logs = AuditLogService(session)

    async def create(self, *, user_id: str, data: dict) -> Incident:
        await self.permissions.require_role(
            organization_id=data["organization_id"], user_id=user_id
        )
        incident = await self.repository.create_incident(data=data)
        await self.audit_logs.record(
            action="incident_created",
            organization_id=incident.organization_id,
            actor_id=user_id,
            target_type="incident",
            target_id=incident.id,
        )
        return incident

    async def list(
        self, *, user_id: str, organization_id: str | None
    ) -> list[Incident]:
        if organization_id:
            await self.permissions.require_role(
                organization_id=organization_id, user_id=user_id
            )
        return await self.repository.list_incidents(
            user_id=user_id, organization_id=organization_id
        )

    async def get(self, *, incident_id: str, user_id: str) -> Incident:
        incident = await self.repository.get_incident_for_user(
            incident_id=incident_id, user_id=user_id
        )
        if incident is None:
            raise NotFoundError("Incident not found.")
        return incident

    async def update(self, *, incident_id: str, user_id: str, data: dict) -> Incident:
        incident = await self.get(incident_id=incident_id, user_id=user_id)
        for field, value in data.items():
            setattr(incident, field, value)
        if incident.status == IncidentStatus.RESOLVED and incident.resolved_at is None:
            incident.resolved_at = datetime.now(UTC)
        return incident

    async def add_timeline(
        self, *, incident_id: str, user_id: str, message: str
    ) -> IncidentTimelineEntry:
        incident = await self.get(incident_id=incident_id, user_id=user_id)
        return await self.repository.create_incident_timeline(
            data={"incident_id": incident.id, "actor_id": user_id, "message": message}
        )
