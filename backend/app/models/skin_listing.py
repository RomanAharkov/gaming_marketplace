from sqlalchemy import CheckConstraint, ForeignKey, String
from app.models.base import Base
from sqlalchemy.orm import mapped_column, Mapped


class SkinListing(Base):
    __tablename__ = "skin_listings"

    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id"), primary_key=True)

    float_value: Mapped[float] = mapped_column(nullable=False)

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    __table_args__ = (
        CheckConstraint(
            "float_value >= 0 AND float_value <= 1",
            name="float_value_range"
        ),
    )