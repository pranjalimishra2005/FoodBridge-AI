from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from backend.models.claim import ClaimStatus


class ClaimCreate(BaseModel):
    donation_id: int


class ClaimResponse(BaseModel):
    id: int
    donation_id: int
    ngo_id: int
    status: ClaimStatus
    claimed_at: datetime
    confirmed_at: Optional[datetime] = None

    class Config:
        from_attributes = True