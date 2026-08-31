from app.database import get_db
from app.schemas.user import UserCreate
from app.core.security import get_password_hash, send_verification_email
from app.services.user import register_user
from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.exceptions.user import (
    UserAlreadyExistsError, 
    UsernameIsTakenError, 
    UserVerificationPendingError
)


authRouter = APIRouter()

@authRouter.post('/register')
async def register(session: Annotated[AsyncSession, Depends(get_db)],
                   user_data: Annotated[UserCreate, Body()]):
    username = user_data.username
    email = user_data.email
    hashed_password = get_password_hash(user_data.password)

    try:
        token = await register_user(username, email, hashed_password, session)
        verification_url = f"http://127.0.0.1:8000/register/verify?token={token}"
        send_verification_email(email, verification_url)
    except UserAlreadyExistsError as e:
        pass
    except UsernameIsTakenError as e:
        pass
    except UserVerificationPendingError as e:
        pass


@authRouter.post('/login')
async def login(session: Annotated[AsyncSession, Depends(get_db)],
                form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    pass