from fastapi import Depends, HTTPException, status

from backend.core.security import get_current_user


def require_role(allowed_roles: list):

    async def role_checker(
        current_user=Depends(get_current_user)
    ):

        if current_user.role.value not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Permission denied",
            )

        return current_user

    return role_checker