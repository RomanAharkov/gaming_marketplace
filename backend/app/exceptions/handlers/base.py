from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.base import ResourceNotFoundError, UnauthorizedAccessError


async def resource_not_found_error_handler(
    _: Request,
    exc: ResourceNotFoundError,
):
    return JSONResponse(
        status_code=404,
        content={
            "detail": str(exc)
        }
    )


async def unauthorized_access_error_handler(
    _: Request,
    exc: UnauthorizedAccessError,
):
    return JSONResponse(
        status_code=403,
        content={
            "detail": str(exc)
        }
    )
