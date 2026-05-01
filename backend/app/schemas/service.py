from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from app.models.enums import ServiceFramework, ServiceStatus, ServiceType


class ServiceCreate(BaseModel):
    organization_id: str
    team_id: str | None = None
    name: str = Field(min_length=1, max_length=180)
    description: str | None = Field(default=None, max_length=5000)
    repository_url: HttpUrl
    service_type: ServiceType
    framework: ServiceFramework
    status: ServiceStatus = ServiceStatus.UNKNOWN
    owner_team: str | None = Field(default=None, max_length=180)


class ServiceUpdate(BaseModel):
    team_id: str | None = None
    name: str | None = Field(default=None, min_length=1, max_length=180)
    description: str | None = Field(default=None, max_length=5000)
    repository_url: HttpUrl | None = None
    service_type: ServiceType | None = None
    framework: ServiceFramework | None = None
    status: ServiceStatus | None = None
    owner_team: str | None = Field(default=None, max_length=180)


class ServiceRead(BaseModel):
    id: str
    organization_id: str
    team_id: str | None
    name: str
    slug: str
    description: str | None
    repository_url: str
    service_type: ServiceType
    framework: ServiceFramework
    status: ServiceStatus
    owner_team: str | None
    created_by: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
