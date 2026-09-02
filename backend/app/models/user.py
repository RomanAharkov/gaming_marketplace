from datetime import datetime
from app.models.base import Base
import enum
from sqlalchemy import DateTime, Enum, String, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=True)

    email: Mapped[str] = mapped_column(unique=True, nullable=False)

    hashed_password: Mapped[str] = mapped_column(nullable=False)

    about: Mapped[str] = mapped_column(default="", nullable=False)

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole, name="user_role"), 
        default=UserRole.USER, 
        nullable=False
    )

    verification_token_hash: Mapped[str] = mapped_column(unique=True, nullable=True)

    verification_token_expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    
    is_verified: Mapped[bool] = mapped_column(default=False, nullable=False, server_default="false")

    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False, server_default="false")

    __table_args__ = (
        UniqueConstraint("email", name="uq_user_email"),
        UniqueConstraint("username", name="uq_user_username"),
        UniqueConstraint(
            "verification_token_hash",
            name="uq_user_verification_token",
        )
    )
    
