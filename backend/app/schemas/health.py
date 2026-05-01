from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import ServiceStatus


class HealthCheckRequest(BaseModel):
    status: ServiceStatus = ServiceStatus.HEALTHY
    latency_ms: int = Field(default=96, ge=0, le=30_000)
    message: str = Field(default="Mock health check passed.", max_length=500)


class HealthCheckRead(BaseModel):
    id: str
    environment_id: str
    status: ServiceStatus
    latency_ms: int
    message: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
