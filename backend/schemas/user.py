from typing import Optional
from pydantic import BaseModel, EmailStr
from enum import Enum

class UserRole(str, Enum):
    DONOR = "DONOR"
    NGO = "NGO"
    ADMIN = "ADMIN"

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: UserRole = UserRole.DONOR  # Default, but client can override
class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    role: Optional[str] = "DONOR"

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"