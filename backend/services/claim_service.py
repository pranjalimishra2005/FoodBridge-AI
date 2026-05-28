from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException

from backend.models.claim import Claim, ClaimStatus
from backend.models.donation import Donation
from backend.models.ngo import NGO
from backend.models.user import User


async def create_claim(
    db: AsyncSession,
    donation_id: int,
    current_user: User,
):

    # 1. Get donation
    result = await db.execute(
        select(Donation).where(Donation.id == donation_id)
    )

    donation = result.scalar_one_or_none()

    if not donation:
        raise HTTPException(
            status_code=404,
            detail="Donation not found",
        )

    # 2. Check availability
    if donation.status != "AVAILABLE":
        raise HTTPException(
            status_code=400,
            detail="Donation not available",
        )

    # 3. Fetch NGO manually (ASYNC SAFE)
    ngo_result = await db.execute(
        select(NGO).where(NGO.user_id == current_user.id)
    )

    ngo = ngo_result.scalar_one_or_none()

    if not ngo:
        raise HTTPException(
            status_code=403,
            detail="NGO profile not found",
        )

    # 4. Create claim
    new_claim = Claim(
        donation_id=donation.id,
        ngo_id=ngo.id,
        status=ClaimStatus.PENDING,
    )

    # 5. Update donation status
    donation.status = "CLAIMED"

    db.add(new_claim)

    await db.commit()

    await db.refresh(new_claim)

    return new_claim


async def get_ngo_claims(
    db: AsyncSession,
    ngo_id: int,
):

    result = await db.execute(
        select(Claim).where(Claim.ngo_id == ngo_id)
    )

    return result.scalars().all()