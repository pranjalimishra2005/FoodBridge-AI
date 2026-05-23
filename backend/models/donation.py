from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from datetime import datetime

from db.database import Base


class Donation(Base):
    __tablename__ = "donations"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    donor_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    food_type: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    expiry: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String,
        default="AVAILABLE"
    )

    location: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    donor = relationship("User")