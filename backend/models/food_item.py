from sqlalchemy import (
    String,
    Float,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from backend.db.database import Base


class FoodItem(Base):
    __tablename__ = "food_items"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    category: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    image_url: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    predicted_freshness: Mapped[float] = mapped_column(
        Float,
        nullable=True
    )