from typing import Annotated
from fastapi import APIRouter, Depends, Query
from app.services.email import email_verification, send_verification_email, verification_cancellation, resend_verification_email
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.core.config import settings


authRouter = APIRouter()

@authRouter.get('/register/verify', status_code=200)
async def verify_email(session: Annotated[AsyncSession, Depends(get_db)],
                       token: Annotated[str, Query()]):
    await email_verification(token, session)
    return {"message": "Email verified successfully."}


@authRouter.get('/register/cancel', status_code=200)
async def cancel_verification(session: Annotated[AsyncSession, Depends(get_db)],
                              token: Annotated[str, Query()]):
    await verification_cancellation(token, session)
    return {"message": "Email verification cancelled successfully."}


@authRouter.get('/register/resend', status_code=200)
async def resend_verification(session: Annotated[AsyncSession, Depends(get_db)],
                              token: Annotated[str, Query()]):
    email, new_token = await resend_verification_email(token, session)

    verification_url = f"{settings.APP_URL}/register/verify?token={new_token}"
    cancel_verification_url = f"{settings.APP_URL}/register/cancel?token={new_token}"
    resend_verification_url = f"{settings.APP_URL}/register/resend?token={new_token}"
    
    send_verification_email(
        email,
        verification_url,
        cancel_verification_url,
        resend_verification_url,
    )

    return {"message": "Verification email resent successfully."}