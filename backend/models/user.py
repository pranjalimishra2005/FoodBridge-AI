from datetime import datetime

from sqlalchemy import (
    String,
    DateTime,
    Enum,
)

from sqlalchemy.sql import func

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from backend.db.database import Base

import enum

class UserRole(str, enum.Enum):
    DONOR = "DONOR"
    NGO = "NGO"
    ADMIN = "ADMIN"
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

    role: Mapped[UserRole] = mapped_column(
    Enum(
        UserRole,
        native_enum=False
    ),
    default=UserRole.DONOR,
    nullable=False,
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

    ngo: Mapped["NGO"] = relationship(
    "NGO",
    back_populates="user",
    uselist=False,
    cascade="all, delete-orphan",
    )