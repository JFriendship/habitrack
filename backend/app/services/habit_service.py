from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.habit_repository import create_habit, get_habits_by_user_id, update_habit, get_habit_by_id, delete_habit
from app.models.habit import Habit
from app.schemas.habit import HabitCreate, HabitUpdate


def create_habit_for_user(
    db: Session, habit_create: HabitCreate, user_id: int
) -> Habit:
    return create_habit(
        db=db,
        name=habit_create.name,
        description=habit_create.description,
        user_id=user_id,
    )


def update_user_habit(
    db: Session, habit_id: int, user_id: int, habit_update: HabitUpdate
) -> Habit:
    """
    Updates a user's habit while ensuring the habit is theirs

    Args:
        db: An sqlalchemy.orm database session
        habit_id: The id associated with the habit being updated
        user_id: The user updating the habit
        habit_update: An object containing the new name and description for the habit

    Returns:
        A new and updated Habit object
    """
    habit = get_habit_by_id(db=db, habit_id=habit_id)
    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")

    if habit.user_id != user_id:
        raise HTTPException(status_code=403, detail="Invalid habit access")

    return update_habit(
        db=db, habit=habit, name=habit_update.name, description=habit_update.description
    )

def delete_user_habit(db: Session, habit_id: int, user_id: int):
    habit = get_habit_by_id(db=db, habit_id=habit_id)

    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")

    if habit.user_id != user_id:
        raise HTTPException(status_code=403, detail="Invalid habit access")
    
    delete_habit(db=db, habit=habit)

def get_user_habits(db: Session, user_id: int) -> list[Habit]:
    return get_habits_by_user_id(db=db, user_id=user_id)
