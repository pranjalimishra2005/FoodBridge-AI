from typing import Optional

from pydantic import BaseModel


class NGOCreate(BaseModel):
    name: str
    registration_number: Optional[str] = None
    focus_areas: Optional[str] = None
    capacity_per_day: Optional[int] = None


class NGOResponse(BaseModel):
    id: int
    name: str
    verified: bool

    class Config:
        from_attributes = True