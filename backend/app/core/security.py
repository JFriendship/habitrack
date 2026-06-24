from pwdlib import PasswordHash
from pwdlib.exceptions import UnknownHashError
from datetime import datetime, timedelta, UTC
from app.core.config import settings
import jwt

hasher = PasswordHash.recommended()

def hash_password(unhashed_password: str) -> str:
    return hasher.hash(unhashed_password)

def verify_password(unhashed_password: str, hashed_password: str) -> bool:
    try:
        return hasher.verify(unhashed_password, hashed_password)
    except UnknownHashError:
        return False
    
def create_access_token(subject: str) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {
        "sub": subject,
        "exp": expire
    }

    return jwt.encode(
        payload=payload,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

def decode_access_token(token: str):
    return jwt.decode(
        token, 
        settings.SECRET_KEY, 
        algorithms=[settings.ALGORITHM]
    )