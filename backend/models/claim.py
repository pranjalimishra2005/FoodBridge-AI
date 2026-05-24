from sqlalchemy import (
    ForeignKey,
    String,
    DateTime,
)
from sqlalchemy.sql import func

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from datetime import datetime

from backend.db.database import Base


class Claim(Base):
    __tablename__ = "claims"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    donation_id: Mapped[int] = mapped_column(
        ForeignKey("donations.id"),
        nullable=False
    )

    ngo_id: Mapped[int] = mapped_column(
        ForeignKey("ngos.id"),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String,
        default="PENDING"
    )

    claimed_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now()
    )

    donation = relationship("Donation")
    ngo = relationship("NGO")