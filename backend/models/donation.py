from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey,
    Boolean,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from sqlalchemy.sql import func

from backend.db.database import Base

if TYPE_CHECKING:
    from backend.models.user import User


class Donation(Base):
    __tablename__ = "donations"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    donor_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    food_type: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    expiry: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String,
        default="AVAILABLE",
    )

    location: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    is_deleted: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )

    donor: Mapped["User"] = relationship(
        "User",
        back_populates="donations",
    )