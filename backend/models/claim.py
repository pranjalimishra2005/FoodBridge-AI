from datetime import datetime
import enum

from sqlalchemy import (
    ForeignKey,
    DateTime,
    Enum,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from backend.db.database import Base


class ClaimStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"


class Claim(Base):
    __tablename__ = "claims"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    donation_id: Mapped[int] = mapped_column(
        ForeignKey("donations.id")
    )

    ngo_id: Mapped[int] = mapped_column(
        ForeignKey("ngos.id")
    )

    status: Mapped[ClaimStatus] = mapped_column(
        Enum(ClaimStatus, native_enum=False),
        default=ClaimStatus.PENDING,
    )

    claimed_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    confirmed_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
    )

    donation: Mapped["Donation"] = relationship(
        "Donation",
        back_populates="claims",
    )

    ngo: Mapped["NGO"] = relationship(
        "NGO",
        back_populates="claims",
    )