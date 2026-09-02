from fastapi.security import OAuth2PasswordBearer
from pwdlib import PasswordHash
import secrets
import hashlib

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

password_hash = PasswordHash.recommended()

def get_password_hash(password: str) -> str:
    return password_hash.hash(password)

def get_verification_token_hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()

def generate_verification_token() -> tuple[str]:

    token = secrets.token_urlsafe(32)

    token_hash = get_verification_token_hash(token)

    return token, token_hash