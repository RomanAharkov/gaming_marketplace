from sqlalchemy import CheckConstraint, ForeignKey, String
from app.models.base import Base
from sqlalchemy.orm import mapped_column, Mapped


class ServiceListing(Base):
    __tablename__ = "service_listings"

    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id"), primary_key=True)

    duration: Mapped[int] = mapped_column(nullable=False)

    service_type: Mapped[str] = mapped_column(String(100), nullable=False)
    
    __table_args__ = (
        CheckConstraint(
            "duration >= 0",
            name="duration_range"
        ),
    )