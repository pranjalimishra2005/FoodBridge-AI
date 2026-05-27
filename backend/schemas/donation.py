from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class DonationCreate(BaseModel):
    food_type: str
    quantity: int = Field(gt=0)
    expiry: datetime
    location: str


class DonationUpdate(BaseModel):
    food_type: Optional[str] = None
    quantity: Optional[int] = Field(
        default=None,
        gt=0
    )
    expiry: Optional[datetime] = None
    status: Optional[str] = None
    location: Optional[str] = None


class DonationResponse(BaseModel):
    id: int
    donor_id: int

    food_type: str
    quantity: int

    expiry: datetime
    status: str
    location: str

    created_at: datetime

    class Config:
        from_attributes = True