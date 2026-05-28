from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from backend.db.database import get_db
from backend.core.permissions import require_role
from backend.models.user import User, UserRole
from backend.models.ngo import NGO
from backend.schemas.claim import ClaimCreate, ClaimResponse
from backend.services.claim_service import create_claim, get_ngo_claims

router = APIRouter(
    prefix="/api/v1/claims",
    tags=["Claims"],
)


@router.post(
    "/",
    response_model=ClaimResponse,
    status_code=status.HTTP_201_CREATED,
)
async def claim_donation(
    payload: ClaimCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_role([UserRole.NGO])
    ),
):
    return await create_claim(
        db=db,
        donation_id=payload.donation_id,
        current_user=current_user,
    )


@router.get(
    "/",
    response_model=list[ClaimResponse],
)
async def list_my_claims(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        require_role([UserRole.NGO])
    ),
):

    # Explicit async query for NGO
    result = await db.execute(
        select(NGO).where(
            NGO.user_id == current_user.id
        )
    )

    ngo = result.scalar_one_or_none()

    if not ngo:
        return []

    claims = await get_ngo_claims(
        db=db,
        ngo_id=ngo.id,
    )

    return claims