from fastapi import (
    Depends,
    HTTPException,
    status
)

from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from sqlalchemy.orm import Session

from backend.db.database import get_db

from backend.repositories.user_repository import (
    get_user_by_email
)

from backend.services.auth_service import (
    decode_token
)


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):

    token = credentials.credentials

    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    email = payload.get("sub")

    user = get_user_by_email(
        db,
        email
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user