import pytest
from app.services.user_service import register_user, authenticate_user
from app.services.user_service import EmailAlreadyExistsError, UsernameAlreadyExistsError, EmailDoesNotExistError
from app.schemas.user import UserCreate

def test_register_user_works(db_session):
    user_create = UserCreate(
        username = "JohnDoe42",
        email = "johndoe42@gmail.com",
        password = "johnDaBest4242"
    )
    user = register_user(db=db_session, user_create=user_create)


def test_register_user_breaks(db_session):
    user_create = UserCreate(
        username = "JohnDoe42",
        email = "johndoe42@gmail.com",
        password = "johnDaBest4242"
    )
    user = register_user(db=db_session, user_create=user_create)

    with pytest.raises(EmailAlreadyExistsError):
        user_create = UserCreate(
            username = "JohnathanDoe",
            email = "johndoe42@gmail.com",
            password = "johnieBest"
        )
        user = register_user(db=db_session, user_create=user_create)
    
    with pytest.raises(UsernameAlreadyExistsError):
        user_create = UserCreate(
            username = "JohnDoe42",
            email = "johnieboy42@gmail.com",
            password = "johnDaBest42"
        )
        user = register_user(db=db_session, user_create=user_create)

def test_authenticate_user_works(db_session):
    email = "johndoe42@gmail.com"
    password = "johnDaBest4242"

    # The database should just have a test user already populated
    user_create = UserCreate(
        username = "JohnDoe42",
        email = email,
        password = password
    )
    user = register_user(db=db_session, user_create=user_create)

    authenticated_user = authenticate_user(db=db_session, email=email, password=password)

    assert authenticated_user != None

def test_authenticate_user_breaks(db_session):
    email="nonexistent@email.com"
    password="nonexistent"

    with pytest.raises(EmailDoesNotExistError):
        authenticated_user = authenticate_user(db=db_session, email=email, password=password)


