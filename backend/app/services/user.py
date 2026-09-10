from app.models.user import User
from app.exceptions.auth import (
    IncorrectCredentialsError,
    UserAlreadyExistsError, 
    UsernameIsTakenError, 
    UserVerificationPendingError
)
from app.core.security import generate_verification_token, verify_password
from app.core.config import settings
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_, select, update
from sqlalchemy.exc import IntegrityError


async def register_user(username: str, email: str, hashed_password: str, session: AsyncSession) -> str:
    now = settings.get_current_time()
    expires_at = now + timedelta(hours=1)

    while True:
        token, token_hash = generate_verification_token()

        result = await session.execute(
            update(User)
            .where(
                User.email == email,
                User.is_verified.is_(False),
                or_(
                    User.verification_token_expires_at.is_(None),
                    User.verification_token_expires_at <= now,
                ),
            )
            .values(
                username=username,
                hashed_password=hashed_password,
                verification_token_hash=token_hash,
                verification_token_expires_at=expires_at,
            )
        )

        if result.rowcount:
            return token

        user_state = await session.execute(
            select(
                User.is_verified,
                User.verification_token_expires_at,
            )
            .where(User.email == email)
        )

        state = user_state.one_or_none()

        if state is not None:
            is_verified, token_expires_at = state

            if is_verified:
                raise UserAlreadyExistsError(
                    "User with this email already exists"
                )

            if token_expires_at is not None and token_expires_at > now:
                raise UserVerificationPendingError(
                    "User verification is still pending. "
                    "Please check your email for the verification link."
                )

        try:
            async with session.begin_nested():
                session.add(
                    User(
                        username=username,
                        email=email,
                        hashed_password=hashed_password,
                        verification_token_hash=token_hash,
                        verification_token_expires_at=expires_at,
                    )
                )

                await session.flush()

        except IntegrityError as e:
            constraint_name = e.orig.__cause__.constraint_name

            if constraint_name == "uq_user_username":
                raise UsernameIsTakenError("Username is already taken") from e

            if constraint_name == "uq_user_email":
                continue

            if constraint_name == "uq_user_verification_token":
                continue

            raise

        return token


async def authenticate_user(username: str, password: str, session: AsyncSession):
    user = await session.scalar(
        select(User).where(User.username == username, User.is_deleted.is_(False))
    )

    if user is None:
        raise IncorrectCredentialsError("Incorrect username or password")
    if not user.is_verified:
        raise IncorrectCredentialsError("Incorrect username or password")
    if not verify_password(password, user.hashed_password):
        raise IncorrectCredentialsError("Incorrect username or password")
        
    return user