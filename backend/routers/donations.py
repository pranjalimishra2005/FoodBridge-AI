from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from backend.db.database import get_db
from backend.schemas.donation import (
    DonationCreate,
    DonationUpdate,
    DonationResponse,
)
from backend.repositories.donation_repository import (
    create_donation,
    get_donations,
    get_donation_by_id,
    update_donation,
    delete_donation,
)
from backend.services.donation_service import (
    validate_expiry,
    verify_donation_owner,
)
from backend.core.security import get_current_user

router = APIRouter(
    prefix="/api/v1/donations",
    tags=["Donations"],
)


@router.post(
    "",
    response_model=DonationResponse,
)
async def create_new_donation(
    donation: DonationCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):

    validate_expiry(donation.expiry)

    created_donation = await create_donation(
        db=db,
        donation_data=donation.model_dump(),
        donor_id=current_user.id,
    )

    return created_donation


@router.get("")
async def list_donations(
    page: int = 1,
    per_page: int = 10,
    food_type: str | None = None,
    status: str | None = None,
    db: AsyncSession = Depends(get_db),
):

    skip = (page - 1) * per_page

    donations, total = await get_donations(
        db=db,
        skip=skip,
        limit=per_page,
        food_type=food_type,
        status=status,
    )

    return {
        "success": True,
        "data": donations,
        "total": total,
        "page": page,
        "per_page": per_page,
    }


@router.get(
    "/{donation_id}",
    response_model=DonationResponse,
)
async def get_single_donation(
    donation_id: int,
    db: AsyncSession = Depends(get_db),
):

    donation = await get_donation_by_id(
        db,
        donation_id,
    )

    if not donation:
        raise HTTPException(
            status_code=404,
            detail="Donation not found",
        )

    return donation


@router.put(
    "/{donation_id}",
    response_model=DonationResponse,
)
async def update_existing_donation(
    donation_id: int,
    update_data: DonationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):

    donation = await get_donation_by_id(
        db,
        donation_id,
    )

    if not donation:
        raise HTTPException(
            status_code=404,
            detail="Donation not found",
        )

    verify_donation_owner(
        donation,
        current_user,
    )

    updated = await update_donation(
        db=db,
        donation=donation,
        update_data=update_data.model_dump(
            exclude_unset=True
        ),
    )

    return updated


@router.delete("/{donation_id}")
async def remove_donation(
    donation_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):

    donation = await get_donation_by_id(
        db,
        donation_id,
    )

    if not donation:
        raise HTTPException(
            status_code=404,
            detail="Donation not found",
        )

    verify_donation_owner(
        donation,
        current_user,
    )

    await delete_donation(
        db,
        donation,
    )

    return {
        "success": True,
        "message": "Donation deleted",
    }
