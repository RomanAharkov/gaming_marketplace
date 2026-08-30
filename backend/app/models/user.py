from app.models.base import Base
import enum
from sqlalchemy import Enum, String
from sqlalchemy.orm import mapped_column, Mapped


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    hashed_password: Mapped[str] = mapped_column(nullable=False)

    about: Mapped[str] = mapped_column(default="", nullable=False)

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"), 
        default=UserRole.USER, 
        nullable=False
    )
    
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False, server_default="false")

    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False, server_default="false")
    
