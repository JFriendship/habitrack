from app.core.security import hash_password, verify_password, create_access_token
from app.core.config import settings
import jwt

def test_hash_password():
    password = "testpassword"
    fake_password = "testPassword"
    hashed_password = hash_password(password)

    assert password != hashed_password

    assert verify_password(password, hashed_password) == True
    assert verify_password(fake_password, hashed_password) == False

def test_create_access_token():
    token = create_access_token("24")

    decoded = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM]
    )

    assert decoded["sub"] == "24"