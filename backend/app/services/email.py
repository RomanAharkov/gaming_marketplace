from datetime import timedelta
from sqlalchemy import select, update
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
    token_hash = get_verification_token_hash(token)
    now = settings.get_current_time()

    result = await session.execute(
        update(User)
        .where(
            User.verification_token_hash == token_hash,
            User.verification_token_expires_at >= now,
            User.is_verified.is_(False),
        )
        .values(
            is_verified=True,
            verification_token_hash=None,
            verification_token_expires_at=None,
        )
    )

    if result.rowcount == 0:
        raise InvalidVerificationTokenError(
            "Invalid or expired verification token"
        )


async def verification_cancellation(token: str, session: AsyncSession) -> None:
    token_hash = get_verification_token_hash(token)

    result = await session.execute(
        update(User)
        .where(
            User.verification_token_hash == token_hash
        )
        .values(
            verification_token_hash=None,
            verification_token_expires_at=None,
        )
    )

    if result.rowcount == 0:
        raise InvalidVerificationTokenError(
            "Cancellation unsuccessful. Invalid verification token"
        )


async def resend_verification_email(token: str, session: AsyncSession) -> tuple[str, str]:
    old_token_hash = get_verification_token_hash(token)
    new_token, new_token_hash = generate_verification_token()

    result = await session.execute(
        update(User)
        .where(
            User.verification_token_hash == old_token_hash
        )
        .values(
            verification_token_hash=new_token_hash,
            verification_token_expires_at=(
                settings.get_current_time() + timedelta(hours=1)
            ),
        )
        .returning(User.email)
    )

    email = result.scalar_one_or_none()

    if email is None:
        raise InvalidVerificationTokenError(
            "Resend unsuccessful. Invalid verification token"
        )

    return email, new_token

        
        
