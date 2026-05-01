from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AuditLogRead(BaseModel):
    id: str
    organization_id: str | None
    workspace_id: str | None
    actor_id: str | None
    action: str
    target_type: str | None
    target_id: str | None
    metadata: dict[str, Any] = Field(
        validation_alias="metadata_json",
        serialization_alias="metadata",
    )
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
