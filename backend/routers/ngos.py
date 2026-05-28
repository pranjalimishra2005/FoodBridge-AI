from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.db.database import get_db
from backend.core.security import get_current_user
from backend.models.user import User
from backend.schemas.ngo import NGOCreate
# Import only from the service layer
from backend.services.ngo_services import create_ngo, get_ngos

router = APIRouter(prefix="/api/v1/ngos", tags=["NGOs"])

@router.post("/")
async def create_ngo_profile(
    payload: NGOCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ngo = await create_ngo(db=db, ngo_data=payload, current_user=current_user)
    return {"success": True, "data": ngo}

@router.get("/")
async def list_ngos(db: AsyncSession = Depends(get_db)):
    ngos = await get_ngos(db)
    return {"success": True, "data": ngos}