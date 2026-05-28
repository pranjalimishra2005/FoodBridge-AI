from datetime import datetime
from typing import List

from sqlalchemy import (
    String,
    DateTime,
    ForeignKey,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from sqlalchemy.sql import func

from backend.db.database import Base


class Donation(Base):
    __tablename__ = "donations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    donor_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    food_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    quantity: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String,
        default="AVAILABLE",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )

    donor: Mapped["User"] = relationship(
        "User",
        back_populates="donations",
    )

    claims: Mapped[List["Claim"]] = relationship(
        "Claim",
        back_populates="donation",
        cascade="all, delete-orphan",
    )