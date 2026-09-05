from datetime import timedelta
from sqlalchemy import select
from app.core.config import settings
from app.models.user import User
from app.core.security import generate_verification_token, get_verification_token_hash
from app.exceptions.auth import InvalidVerificationTokenError
from pathlib import Path
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
import resend


resend.api_key = settings.API_KEY

TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "html" 

def load_html(template_name: str, **context) -> str:
    template_path = TEMPLATES_DIR / template_name

    html = template_path.read_text(encoding="latin-1")

    for key, value in context.items():
        html = html.replace("{" + key + "}", str(value))

    return html

def send_verification_email(email: EmailStr, verification_url: str, cancel_verification_url: str, resend_verification_url: str) -> None:

    html = load_html(
        "verify_email.html",
        verification_url=verification_url,
        resend_verification_url=resend_verification_url,
        cancel_verification_url=cancel_verification_url,
    )

    params = {
        "from": "noreply@support.domish.org",
        "to": [str(email)],
        "subject": "Email verification",
        "html": html,
    }

    email = resend.Emails.send(params)


async def email_verification(token: str, session: AsyncSession) -> None:

    user = await session.scalar(
        select(User).where(User.verification_token_hash == get_verification_token_hash(token))
    )

    if user is None:
        raise InvalidVerificationTokenError("Invalid verification token")

    if user.verification_token_expires_at < settings.get_current_time():
        raise InvalidVerificationTokenError("Verification token has expired")

    user.is_verified = True
    user.verification_token_hash = None
    user.verification_token_expires_at = None

    await session.flush()


async def verification_cancellation(token: str, session: AsyncSession) -> None:

    user = await session.scalar(
        select(User).where(User.verification_token_hash == get_verification_token_hash(token))
    )

    if user is None:
        raise InvalidVerificationTokenError("Cancellation unsuccessful. Invalid verification token")

    user.verification_token_hash = None
    user.verification_token_expires_at = None

    await session.flush()


async def resend_verification_email(token: str, session: AsyncSession) -> tuple[str, str]:

    user = await session.scalar(
        select(User).where(User.verification_token_hash == get_verification_token_hash(token))
    )

    if user is None:
        raise InvalidVerificationTokenError("Resend unsuccessful. Invalid verification token")

    token, token_hash = generate_verification_token()

    user.verification_token_expires_at = settings.get_current_time() + timedelta(hours=1)
    user.verification_token_hash = token_hash

    await session.flush()

    return user.email, token

        
        
