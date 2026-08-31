from app.models.user import User
from app.exceptions.user import (
    UserAlreadyExistsError, 
    UsernameIsTakenError, 
    UserVerificationPendingError
)
from app.core.security import generate_verification_token
from datetime import UTC, datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError




async def register_user(username: str, email: str, hashed_password: str, session: AsyncSession) -> str:

    async with session.begin():

        existing_user = await session.scalar(
            select(User).where(User.email == email)
        )

        if existing_user is not None:

            if existing_user.is_verified:
                raise UserAlreadyExistsError()

            if existing_user.verification_token_expires_at > datetime.now(UTC):
                raise UserVerificationPendingError()

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
                            verification_token_expires_at = datetime.now(UTC) + timedelta(hours=1)
                        )
                        session.add(user)

                    else:
                        existing_user.username = username
                        existing_user.hashed_password = hashed_password
                        existing_user.verification_token_hash = token_hash
                        existing_user.verification_token_expires_at = datetime.now(UTC) + timedelta(hours=1)

                    await session.flush()

            except IntegrityError as e:
                constraint = getattr(e.orig, "constraint_name", None)
                if constraint == "uq_user_username":
                    raise UsernameIsTakenError() from e
                elif constraint == "uq_user_verification_token":
                    continue
                raise
            return token
                