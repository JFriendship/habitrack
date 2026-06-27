from datetime import date
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.habit_completion import HabitCompletion

def create_completion(db: Session, habit_id: int, completed_date: date) -> HabitCompletion:
    completion = HabitCompletion(habit_id=habit_id, completed_date=completed_date)

    db.add(completion)
    db.commit()
    db.refresh(completion)

    return completion

def get_completion_for_habit_and_date(db: Session, habit_id: int, completed_date: date) -> HabitCompletion | None:
    stmt = select(HabitCompletion).where(HabitCompletion.habit_id == habit_id, HabitCompletion.completed_date == completed_date)

    return db.scalar(stmt)

def get_completions_for_habit_id(db: Session, habit_id: int) -> list[HabitCompletion]:
    stmt = (select(HabitCompletion).where(HabitCompletion.habit_id == habit_id).order_by(HabitCompletion.completed_date.desc()))

    return list(db.scalars(stmt).all())

def delete_completion(db: Session, completion: HabitCompletion) -> None:
    db.delete(completion)
    db.commit()

def completion_exists_for_habit_and_date(db: Session, habit_id: int, completed_date: date) -> bool:
    stmt = select(HabitCompletion.id).where(HabitCompletion.habit_id == habit_id, HabitCompletion.completed_date == completed_date)

    return db.scalar(stmt) is not None
