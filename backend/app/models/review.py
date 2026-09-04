from datetime import datetime
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped
from app.models.base import Base
from app.core.config import settings


class Review(Base):
    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(primary_key=True)

    rating: Mapped[int] = mapped_column(nullable=False)

    description: Mapped[str] = mapped_column(String(500), nullable=False)

    seller_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    buyer_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)

    created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), 
            default=settings.get_current_time, 
            nullable=False
    )

    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False, server_default="false")

    __table_args__ = (
        CheckConstraint("rating BETWEEN 1 AND 5", name="rating_between_1_and_5"),
    )