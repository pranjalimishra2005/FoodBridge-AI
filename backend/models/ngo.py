from typing import Optional, List

from sqlalchemy import (
    String,
    Boolean,
    ForeignKey,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from backend.db.database import Base


class NGO(Base):
    __tablename__ = "ngos"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id")
    )

    name: Mapped[str] = mapped_column(
        String,
        nullable=False,
    )

    registration_number: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    focus_areas: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    capacity_per_day: Mapped[Optional[int]] = mapped_column(
        nullable=True,
    )

    verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )

    latitude: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    longitude: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
    )

    user: Mapped["User"] = relationship(
        "User",
        back_populates="ngo",
    )

    claims: Mapped[List["Claim"]] = relationship(
        "Claim",
        back_populates="ngo",
        cascade="all, delete-orphan",
    )