from pydantic import BaseModel, ConfigDict, EmailStr, Field
from app.models.user import UserRole


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    about: str
    role: UserRole
    is_verified: bool
    is_deleted: bool

    model_config = ConfigDict(from_attributes=True)