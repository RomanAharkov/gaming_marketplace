from pwdlib import PasswordHash
import secrets
import hashlib
import jwt
from app.models.user import User
from app.core.config import settings

password_hash = PasswordHash.recommended()

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return password_hash.verify(plain_password, hashed_password)

def get_verification_token_hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def generate_verification_token() -> tuple[str]:
    token = secrets.token_urlsafe(32)
    token_hash = get_verification_token_hash(token)
    return token, token_hash

def create_access_token(user: User) -> str:
    expire = settings.get_current_time() + settings.get_access_token_expire_minutes()
    payload = {
        "sub": str(user.id),
        "exp": expire
    }
    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
