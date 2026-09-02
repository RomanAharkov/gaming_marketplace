from app.models.user import User
from app.exceptions.auth import (
    UserAlreadyExistsError, 
    UsernameIsTakenError, 
    UserVerificationPendingError
)
from app.core.security import generate_verification_token
from app.core.config import settings
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from asyncpg import UniqueViolationError


async def register_user(username: str, email: str, hashed_password: str, session: AsyncSession) -> str:

    async with session.begin():

        existing_user = await session.scalar(
            select(User).where(User.email == email)
        )

        if existing_user is not None:

            if existing_user.is_verified:
                raise UserAlreadyExistsError("User with this email already exists")

            if (existing_user.verification_token_expires_at is not None 
                and existing_user.verification_token_expires_at > settings.get_current_time()):
                raise UserVerificationPendingError("User verification is still pending. Please check your email for the verification link.")

        while True:
            try:
                async with session.begin_nested():

                    token, token_hash = generate_verification_token()

                    if existing_user is None:
                        user = User(
                            username = username,
                            email = email,
                            hashed_password = hashed_password,
                            verification_token_hash = token_hash,
                            verification_token_expires_at = settings.get_current_time() + timedelta(hours=1)
                        )
                        session.add(user)

                    else:
                        existing_user.username = username
                        existing_user.hashed_password = hashed_password
                        existing_user.verification_token_hash = token_hash
                        existing_user.verification_token_expires_at = settings.get_current_time() + timedelta(hours=1)

                    await session.flush()

            except IntegrityError as e:
                uv_eror = e.orig.__cause__
                constraint_name = uv_eror.constraint_name
                if constraint_name == "uq_user_username":
                    raise UsernameIsTakenError("Username is already taken") from e
                elif constraint_name == "uq_user_verification_token":
                    continue
                raise
            return token
                