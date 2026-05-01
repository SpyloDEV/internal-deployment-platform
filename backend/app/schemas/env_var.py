from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EnvVarCreate(BaseModel):
    key: str = Field(min_length=1, max_length=180, pattern=r"^[A-Z0-9_]+$")
    value: str = Field(min_length=1, max_length=5000)
    is_secret: bool = True


class EnvVarUpdate(BaseModel):
    value: str | None = Field(default=None, min_length=1, max_length=5000)
    is_secret: bool | None = None


class EnvVarRead(BaseModel):
    id: str
    environment_id: str
    key: str
    value_masked: str
    is_secret: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
