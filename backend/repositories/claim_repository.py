from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.claim import Claim

async def create_claim(
    db: AsyncSession,
    donation_id: int,
    ngo_id: int
) -> Claim:
    """
    Handles the instantiation and persistence of a new claim.
    """
    new_claim = Claim(
        donation_id=donation_id,
        ngo_id=ngo_id,
        status="PENDING" # Explicitly set initial state
    )
    db.add(new_claim)
    await db.commit()
    await db.refresh(new_claim)
    return new_claim

async def get_claim_by_donation(
    db: AsyncSession,
    donation_id: int,
) -> Claim | None:
    result = await db.execute(
        select(Claim).where(Claim.donation_id == donation_id)
    )
    return result.scalar_one_or_none()