from fastapi import Request
from fastapi.responses import JSONResponse
from app.exceptions.auth import IncorrectCredentialsError, InvalidVerificationTokenError, RegistrationError


async def registration_error_handler(
    _: Request,
    exc: RegistrationError,
):
    return JSONResponse(
        status_code=409,
        content={
            "detail": str(exc)
        }
    )

async def invalid_verification_token_error_handler(
    _: Request,
    exc: InvalidVerificationTokenError,
):
    return JSONResponse(
        status_code=400,
        content={
            "detail": str(exc)
        }
    )

async def incorrect_credentials_error_handler(
    _: Request,
    exc: IncorrectCredentialsError,
):
    return JSONResponse(
        status_code=401,
        content={
            "detail": str(exc)
        }
    )