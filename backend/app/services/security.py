from pwdlib import PasswordHash
from pwdlib.exceptions import UnknownHashError

hasher = PasswordHash.recommended()

def hash_password(unhashed_password: str) -> str:
    return hasher.hash(unhashed_password)

def verify_password(unhashed_password: str, hashed_password: str) -> bool:
    try:
        return hasher.verify(unhashed_password, hashed_password)
    except UnknownHashError:
        return False