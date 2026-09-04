from app.database import get_db
from app.schemas.auth import LoginResponse, RegistrationRequest, RegistrationResponse
from app.core.security import create_access_token, get_password_hash
from app.core.config import settings
from app.services.email import send_verification_email
from app.services.user import authenticate_user, register_user
from fastapi import APIRouter, BackgroundTasks, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated


authRouter = APIRouter()

@authRouter.post('/register', status_code=201, response_model=RegistrationResponse)
async def register(background_tasks: BackgroundTasks,
                   session: Annotated[AsyncSession, Depends(get_db)],
                   user_data: Annotated[RegistrationRequest, Body()]):
    username = user_data.username
    email = user_data.email
    hashed_password = get_password_hash(user_data.password)

    token = await register_user(username, email, hashed_password, session)

    verification_url = f"{settings.APP_URL}/register/verify?token={token}"
    cancel_verification_url = f"{settings.APP_URL}/register/cancel?token={token}"
    resend_verification_url = f"{settings.APP_URL}/register/resend?token={token}"

    background_tasks.add_task(
        send_verification_email,
        user_data.email,
        verification_url,
        cancel_verification_url,
        resend_verification_url,
    )

    return RegistrationResponse(
        message="Registration successful. Please check your email to verify your account."
    )


@authRouter.post('/login', response_model=LoginResponse)
async def login(session: Annotated[AsyncSession, Depends(get_db)],
                form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    username = form_data.username
    password = form_data.password

    user = await authenticate_user(username, password, session)

    token = create_access_token(user)

    return LoginResponse(
        access_token=token,
        token_type="bearer"
    )

