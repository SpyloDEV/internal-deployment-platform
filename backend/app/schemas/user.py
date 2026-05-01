from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr

from app.models.enums import UserRole


class UserRead(BaseModel):
    id: str
    email: EmailStr
    full_name: str | None
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
