from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import IncidentSeverity, IncidentStatus


class IncidentCreate(BaseModel):
    organization_id: str
    service_id: str | None = None
    environment_id: str | None = None
    deployment_id: str | None = None
    title: str = Field(min_length=1, max_length=240)
    severity: IncidentSeverity
    status: IncidentStatus = IncidentStatus.OPEN


class IncidentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=240)
    severity: IncidentSeverity | None = None
    status: IncidentStatus | None = None
    resolved_at: datetime | None = None


class IncidentRead(BaseModel):
    id: str
    organization_id: str
    service_id: str | None
    environment_id: str | None
    deployment_id: str | None
    title: str
    severity: IncidentSeverity
    status: IncidentStatus
    started_at: datetime
    resolved_at: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class IncidentTimelineCreate(BaseModel):
    message: str = Field(min_length=1, max_length=5000)


class IncidentTimelineRead(BaseModel):
    id: str
    incident_id: str
    actor_id: str | None
    message: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
