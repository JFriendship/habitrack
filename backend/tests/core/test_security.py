from app.core.security import hash_password, verify_password

def test_hash_password():
    password = "testpassword"
    fake_password = "testPassword"
    hashed_password = hash_password(password)

    assert password != hashed_password

    assert verify_password(password, hashed_password) == True
    assert verify_password(fake_password, hashed_password) == False