from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.user import User
from backend.schemas.ngo import NGOCreate
from backend.repositories.ngo_repository import create_ngo as repo_create_ngo, get_ngos as repo_get_ngos

async def create_ngo(db: AsyncSession, ngo_data: NGOCreate, current_user: User):
    # Business Logic: Use the user object to enforce ownership
    data_dict = ngo_data.model_dump()
    return await repo_create_ngo(db, data_dict, user_id=current_user.id)

async def get_ngos(db: AsyncSession):
    return await repo_get_ngos(db)