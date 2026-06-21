from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User

def get_user_by_email(db: Session, email: str) -> User | None:
    """
    Check if a user email exists in the database and returns the user.

    Args:
        db: A database connection
        email: A user's email
    
    Returns:
        A User's database information or None
    """

    stmt = select(User).where(User.email == email)

    return db.scalar(stmt)  # returns None if the user isn't found

def get_user_by_username(db: Session, username: str) -> User | None:
    """
    Check if a user username exists in the database and returns the user.

    Args:
        db: A database connection
        username: A user's username
    
    Returns:
        A User's database information or None
    """

    stmt = select(User).where(User.username == username)

    return db.scalar(stmt)

def get_user_by_id(db: Session, user_id: int) -> User | None:
    """
    Check if a user id exists in the database and returns the user.

    Args:
        db: A database connection
        user_id: A user's id
    
    Returns:
        A User's database information or None
    """
    
    stmt = select(User).where(User.id == user_id)

    return db.scalar(stmt)  # returns None if the user isn't found

def create_user(db: Session, username: str, email: str, hashed_password: str) -> User:
    """
    Insert a new user into the database.

    Args:
        db: A database connection
        username: The new user's uesrname
        email: The new user's email address
        hashed_password: The new user's already hashed password

    Returns:
        The newly created User object
    """

    user = User(username=username, email=email, hashed_password=hashed_password)

    db.add(user)
    db.commit()
    db.refresh(user)

    return user
