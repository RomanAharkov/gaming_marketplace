from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
import os
from dotenv import load_dotenv
import secrets
import hashlib
import resend

load_dotenv()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

resend.api_key = f'{os.getenv("API_KEY")}'

password_hash = PasswordHash.recommended()

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def generate_verification_token() -> tuple[str]:

    token = secrets.token_urlsafe(32)

    token_hash = hashlib.sha256(
        token.encode()
    ).hexdigest()

    return token, token_hash

def send_verification_email(email, verification_url):
    params = {
        "from": "noreply@yourdomain.com",
        "to": [f"{email}"],
        "subject": "Email verification",
        "html": f"""
            <h1>Verify your email</h1>
            <p>Click the link below to verify your account:</p>
            <a href="{verification_url}">
                Verify email
            </a>
        """,
    }

    email = resend.Emails.send(params)