from starlette.middleware.base import BaseHTTPMiddleware

from fastapi import Request

from fastapi.responses import JSONResponse

from backend.services.auth_service import decode_token


EXCLUDED_PATHS = [
    "/docs",
    "/openapi.json",
    "/api/v1/auth/register",
    "/api/v1/auth/login"
]


class AuthMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self,
        request: Request,
        call_next
    ):

        path = request.url.path

        if path in EXCLUDED_PATHS:
            return await call_next(request)

        auth_header = request.headers.get(
            "Authorization"
        )

        if not auth_header:
            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Authorization header missing"
                }
            )

        try:

            scheme, token = auth_header.split()

            if scheme.lower() != "bearer":
                raise ValueError()

        except ValueError:

            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Invalid authorization format"
                }
            )

        payload = decode_token(token)

        if not payload:
            return JSONResponse(
                status_code=401,
                content={
                    "detail": "Invalid or expired token"
                }
            )

        response = await call_next(request)

        return response