from app.models.base import Base
from sqlalchemy.orm import mapped_column, Mapped


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(nullable=False)