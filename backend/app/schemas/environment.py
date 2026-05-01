from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from app.models.enums import EnvironmentName, ServiceStatus


class EnvironmentCreate(BaseModel):
    name: EnvironmentName
    branch: str = Field(default="main", min_length=1, max_length=180)
    base_url: HttpUrl | None = None
    status: ServiceStatus = ServiceStatus.UNKNOWN
    auto_deploy_enabled: bool = False


class EnvironmentUpdate(BaseModel):
    branch: str | None = Field(default=None, min_length=1, max_length=180)
    base_url: HttpUrl | None = None
    status: ServiceStatus | None = None
    auto_deploy_enabled: bool | None = None


class EnvironmentRead(BaseModel):
    id: str
    service_id: str
    name: EnvironmentName
    branch: str
    base_url: str | None
    status: ServiceStatus
    auto_deploy_enabled: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
