from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=1, max_length=180)
    slug: str | None = Field(default=None, min_length=2, max_length=180)


class OrganizationUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=180)


class OrganizationRead(BaseModel):
    id: str
    name: str
    slug: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TeamCreate(BaseModel):
    organization_id: str
    name: str = Field(min_length=1, max_length=180)
    slug: str | None = Field(default=None, min_length=2, max_length=180)


class TeamUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=180)


class TeamRead(BaseModel):
    id: str
    organization_id: str
    name: str
    slug: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
