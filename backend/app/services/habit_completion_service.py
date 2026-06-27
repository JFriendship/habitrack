from datetime import date, datetime, UTC
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.habit_repository import get_habit_by_id
from app.repositories.habit_completion_repositories import (
    completion_exists_for_habit_and_date,
    create_completion,
    delete_completion,
    get_completions_for_habit_id,
    get_completion_for_habit_and_date,
)

def _get_habit_or_raise(db: Session, habit_id: int, user_id: int):
    """
    Gets a habit and checks to make sure it exists and is being accessed by the correct user

    Args:
        db: An sqlalchemy.orm database Session
        habit_id: The id of the habit being accessed
        user_id: The id of the user requesting access to the habit
    """
    habit = get_habit_by_id(db=db, habit_id=habit_id)

    if habit is None:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    if habit.user_id != user_id:
        raise HTTPException(status_code=403, detail="Invalid habit credentials")
    
    return habit

def mark_habit_complete(db: Session, habit_id: int, user_id: int, completed_date: date | None = None):
    _get_habit_or_raise(db=db, habit_id=habit_id, user_id=user_id)

    completed_date = completed_date or datetime.now(UTC).date()

    existing_completion = get_completion_for_habit_and_date(db=db, habit_id=habit_id, completed_date=completed_date)

    if existing_completion is not None:
        return existing_completion

    return create_completion(db=db, habit_id=habit_id, completed_date=completed_date)

def unmark_habit_complete(db: Session, habit_id: int, user_id: int,  completed_date: date):
    # Make sure user owns the habit and that the habit exists
    _get_habit_or_raise(db=db, habit_id=habit_id, user_id=user_id)

    completion = get_completion_for_habit_and_date(db=db, habit_id=habit_id, completed_date=completed_date)

    if completion is None:
        raise HTTPException(status_code=404, detail="Habit completion not found")

    delete_completion(db=db, completion=completion)

def get_habit_completion_history(db: Session, habit_id: int, user_id: int):
    _get_habit_or_raise(db=db, habit_id=habit_id, user_id=user_id)

    return get_completions_for_habit_id(db=db, habit_id=habit_id)

def habit_completed_on_date(db: Session, habit_id: int, user_id: int, completed_date: date) -> bool:
    _get_habit_or_raise(db=db, habit_id=habit_id, user_id=user_id)

    return completion_exists_for_habit_and_date(db=db, habit_id=habit_id, completed_date=completed_date)
