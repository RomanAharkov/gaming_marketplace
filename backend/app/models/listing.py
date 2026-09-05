import enum
from datetime import datetime
from decimal import Decimal
from sqlalchemy import CheckConstraint, DateTime, Enum, ForeignKey, Numeric, String
from app.models.base import Base
from sqlalchemy.orm import mapped_column, Mapped
from app.core.config import settings

class ListingStatus(str, enum.Enum):
    OPEN = "open"
    CLOSED = "closed"
    DELETED = "deleted"

class Listing(Base):
    __tablename__ = 'listings'

    id: Mapped[int] = mapped_column(primary_key=True)
    
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    description: Mapped[str] = mapped_column(String(500), nullable=False, default="")

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)

    seller_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    
    game_id: Mapped[int] = mapped_column(ForeignKey("games.id"), nullable=False)

    status: Mapped[ListingStatus] = mapped_column(
            Enum(ListingStatus, name="listing_status"), 
            default=ListingStatus.OPEN, 
            nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        default=settings.get_current_time, 
        nullable=False
    )

    __table_args__ = (
        CheckConstraint(
            "price >= 0",
            name="price_range"
        ),
    )
    