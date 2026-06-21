from app.repositories.user_repository import get_user_by_email, get_user_by_id, create_user

# Make sure the database updates
def test_get_user_by_email(db_session):
    assert(get_user_by_email(db_session, "fake_email@gmail.com") == None)

def test_get_user_by_id(db_session):
    assert(get_user_by_id(db_session, -1) == None)

def test_create_user(db_session):
    user = create_user(
        db=db_session,
        username="tester2",
        email="test2@example.com",
        hashed_password="hashed_pw"
    )

    assert user.id is not None
    assert user.email == "test2@example.com"

    db_user = get_user_by_email(
        db=db_session,
        email="test2@example.com"
    )

    assert db_user is not None
    assert db_user.email == "test2@example.com"
    