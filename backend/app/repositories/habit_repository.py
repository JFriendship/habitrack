from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.habit import Habit

def create_habit(db: Session, name: str, description: str | None, user_id: int) -> Habit:
    """
    Creates a new Habit object and stores it in the database

    Args:
        db: An sqlalchemy.orm database session
        name: The new habit's name
        description: The description of the new habit
        user_id: The user id for the creator of the new habit

    Returns:
        The newly create Habit object
    """

    habit = Habit(name=name, description=description, user_id=user_id)

    db.add(habit)
    db.commit()
    db.refresh(habit)

    return habit

def update_habit(db: Session, habit: Habit, name: str, description: str) -> Habit:
    """
    Updates a preexisting habit in the database

    Args:
        db:
        habit: The habit object containing the preexisting habit's information
        name: The new name for the habit
        description: The new description for the habit

    Returns:
        The newly updated habit object

    """
    habit.name = name
    habit.description = description

    db.commit()
    db.refresh(habit)

    return habit

def delete_habit(db: Session, habit: Habit) -> None:
    """
    Deletes a habit from the database

    Args:
        db: An sqlalchemy.orm database session
        habit: The habit to be deleted
    """
    db.delete(habit)
    db.commit()

def get_habits_by_user_id(
        db: Session,
        user_id: int,
) -> list[Habit]:
    """
    Retrieves all the habits owned by a user

    Args:
        db: An sqlalchemy.orm database session
        user_id: The id of the user
    
    Returns:
        A list of Habit objects associated with the provided user id
    """
    stmt = select(Habit).where(Habit.user_id == user_id)

    return list(db.scalars(stmt).all())

def get_habit_by_id(db: Session, habit_id: int) -> Habit | None:
    """
    Retrieve a single habit

    Args:
        db: An sqlalchemy.orm database session
        habit_id: The id of a habit in the database
    
    Returns:
        A Habit object that contains the habit's information
    """
    return db.get(Habit, habit_id)

