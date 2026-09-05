import enum
from datetime import datetime
from decimal import Decimal
from sqlalchemy import DateTime, Enum, ForeignKey, Numeric
from app.models.base import Base
from app.core.config import settings
from sqlalchemy.orm import mapped_column, Mapped


class OrderStatus(str, enum.Enum):
    COMPLETED = 'completed'
    FAILED = 'failed'


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)

    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id"), nullable=False)

    review_id: Mapped[int] = mapped_column(ForeignKey("reviews.id"), nullable=True, default=None)

    buyer_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    status: Mapped[OrderStatus] = mapped_column(
        Enum(OrderStatus, name="order_status"),
        nullable=True 
    )

    created_at: Mapped[datetime] = mapped_column(
            DateTime(timezone=True), 
            default=settings.get_current_time, 
            nullable=False
    )

    is_deleted: Mapped[bool] = mapped_column(default=False, nullable=False, server_default="false")

