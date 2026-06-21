from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.repositories.user_repository import get_user_by_email, get_user_by_username, create_user
from app.core.security import hash_password, verify_password

def register_user(db: Session, user_create: UserCreate) -> User | None:
    """
        Registers a new user into the database.

        Args:
            db: The database session
            user_create: Contains the user's username, email, and password information.

        Returns:
            A new User object with the user's information or None
    """
    if get_user_by_email(db, user_create.email):
        raise EmailAlreadyExistsError
    elif get_user_by_username(db, user_create.username):
        raise UsernameAlreadyExistsError
    else:
        # Hash the password and insert the new user into the database
        hashed_password = hash_password(user_create.password)
        user = create_user(
            db=db,
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password,
        )
        return user

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    """
    Authenticate a user by verifying their email and password

    Args:
        db: The users database session
        email: The user's email address
        password: The user's unhashed password

    Returns:
        The User object with the user's information if the user has been authenticated.
        Otherwise, it will return None.
    """
    user = get_user_by_email(db=db, email=email)

    if user:
        if verify_password(password, user.hashed_password):
            return user
        else:
            return None
    else:
        raise EmailDoesNotExistError


# Exceptions
class EmailAlreadyExistsError(Exception):
    """The provided email already exists in the database"""
    pass

class UsernameAlreadyExistsError(Exception):
    """The provided username already exists in the database"""
    pass

class EmailDoesNotExistError(Exception):
    """The provided email does not exist in the database"""
    pass