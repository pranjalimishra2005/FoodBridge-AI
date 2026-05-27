from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models.donation import Donation


async def create_donation(
    db: AsyncSession,
    donation_data: dict,
    donor_id: int,
):
    donation = Donation(
        **donation_data,
        donor_id=donor_id,
    )

    db.add(donation)

    await db.commit()

    await db.refresh(donation)

    return donation


async def get_donations(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    food_type: str | None = None,
    status: str | None = None,
):
    query = select(Donation).where(
        Donation.is_deleted == False
    )

    if food_type:
        query = query.where(
            Donation.food_type.ilike(
                f"%{food_type}%"
            )
        )

    if status:
        query = query.where(
            Donation.status == status
        )

    total_query = select(func.count()).select_from(
        query.subquery()
    )

    total_result = await db.execute(total_query)
    total = total_result.scalar()

    query = (
        query
        .offset(skip)
        .limit(limit)
    )

    result = await db.execute(query)

    donations = result.scalars().all()

    return donations, total


async def get_donation_by_id(
    db: AsyncSession,
    donation_id: int,
):
    query = select(Donation).where(
        Donation.id == donation_id,
        Donation.is_deleted == False,
    )

    result = await db.execute(query)

    return result.scalars().first()


async def update_donation(
    db: AsyncSession,
    donation: Donation,
    update_data: dict,
):
    for key, value in update_data.items():
        setattr(donation, key, value)

    await db.commit()

    await db.refresh(donation)

    return donation


async def delete_donation(
    db: AsyncSession,
    donation: Donation,
):
    donation.is_deleted = True

    await db.commit()

    await db.refresh(donation)

    return donation