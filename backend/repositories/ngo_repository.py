from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.ngo import NGO

async def create_ngo(db: AsyncSession, ngo_data: dict, user_id: int):
    ngo = NGO(**ngo_data, user_id=user_id)
    db.add(ngo)
    await db.commit()
    await db.refresh(ngo)
    return ngo

async def get_ngos(db: AsyncSession):
    result = await db.execute(select(NGO))
    return result.scalars().all()