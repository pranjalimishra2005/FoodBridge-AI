from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.database import get_db

from backend.schemas.user import (
    UserCreate,
    UserLogin,
    UserResponse,
    TokenResponse,
)

from backend.repositories.user_repository import (
    get_user_by_email,
    create_user,
)

from backend.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
)

from backend.core.config import settings


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


# ----------------------------------------
# REGISTER USER
# ----------------------------------------
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db),
):

    existing_user = await get_user_by_email(db, user.email)

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    hashed_password = hash_password(user.password)

    user_data = {
        "email": user.email,
        "hashed_password": hashed_password,
        "role": user.role,
    }

    new_user = await create_user(db, user_data)
    # 1. Refresh the object to ensure all DB defaults (like 'id' and 'created_at') are loaded
    await db.refresh(new_user)
    # 2. Return the model directly. 
    # Because you set 'from_attributes = True' in your schema, 
    # Pydantic will automatically map the SQLAlchemy fields to the response.
    return new_user


# ----------------------------------------
# LOGIN USER
# ----------------------------------------
@router.post(
    "/login",
    response_model=TokenResponse,
)
async def login_user(
    user: UserLogin,
    db: AsyncSession = Depends(get_db),
):

    existing_user = await get_user_by_email(db, user.email)

    # Prevent email enumeration (safe error)
    if not existing_user or not verify_password(
        user.password,
        existing_user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": existing_user.email},
        expires_delta=timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    )

    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )