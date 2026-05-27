from datetime import datetime

from sqlalchemy import (
    String,
    DateTime,
)

from sqlalchemy.sql import func

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from backend.db.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    hashed_password: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    role: Mapped[str] = mapped_column(
        String(50),
        default="DONOR",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
    )

    donations: Mapped[list["Donation"]] = relationship(
        "Donation",
        back_populates="donor",
        cascade="all, delete-orphan",
    )