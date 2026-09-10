from datetime import datetime
from decimal import Decimal
import enum
from app.models.base import Base
from app.core.config import settings
from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Numeric
from sqlalchemy.orm import mapped_column, Mapped


class PaymentType(str, enum.Enum):
    PURCHASE = "purchase"
    DEPOSIT = "deposit"
    REFUND = "refund"


class PaymentStatus(str, enum.Enum):
    COMPLETED = "completed"
    FAILED = "failed"


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=True)

    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    type: Mapped[PaymentType] = mapped_column(
        Enum(PaymentType, name="payment_type"),
        nullable=False
    )

    status: Mapped[PaymentStatus] = mapped_column(
        Enum(PaymentStatus, name="payment_status"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=settings.get_current_time, 
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "amount >= 0",
            name="amount_range"
        ),
    )