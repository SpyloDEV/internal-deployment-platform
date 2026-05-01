from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import DeploymentStatus, LogLevel


class DeploymentCreate(BaseModel):
    version: str | None = Field(default=None, max_length=80)
    commit_sha: str = Field(default="local-mock-commit", min_length=6, max_length=64)
    branch: str | None = Field(default=None, max_length=180)
    force_failure: bool = False


class DeploymentRead(BaseModel):
    id: str
    service_id: str
    environment_id: str
    version: str
    commit_sha: str
    branch: str
    status: DeploymentStatus
    triggered_by: str | None
    started_at: datetime | None
    finished_at: datetime | None
    duration_seconds: int | None
    error_message: str | None
    rollback_source_deployment_id: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class DeploymentLogRead(BaseModel):
    id: str
    deployment_id: str
    level: LogLevel
    step: str | None
    message: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
