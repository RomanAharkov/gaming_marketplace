from sqlalchemy import CheckConstraint, ForeignKey, String
from app.models.base import Base
from sqlalchemy.orm import mapped_column, Mapped


class GameListing(Base):
    __tablename__ = "game_listings"

    listing_id: Mapped[int] = mapped_column(ForeignKey("listings.id"), primary_key=True)

    platform: Mapped[str] = mapped_column(String(50), nullable=False)

    type: Mapped[str] = mapped_column(String(50), nullable=False)