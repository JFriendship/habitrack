from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.habit import HabitCreate, HabitRead, HabitUpdate
from app.schemas.habit_completion import HabitCompletionRead, HabitCompletionStatusRead
from app.services.habit_service import (
    create_habit_for_user,
    get_user_habits,
    update_user_habit,
    delete_user_habit,
)
from app.services.habit_completion_service import (
    mark_habit_complete,
    unmark_habit_complete,
    get_habit_completion_history,
    habit_completed_on_date
)

router = APIRouter(prefix="/habits", tags=["habits"])

@router.post("", response_model=HabitRead, status_code=201)
def create_habit(
    habit: HabitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_habit_for_user(
        db=db,
        habit_create=habit,
        user_id=current_user.id,
    )


@router.get("", response_model=list[HabitRead])
def get_habits(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_user_habits(db=db, user_id=current_user.id)


@router.put("/{habit_id}", response_model=HabitRead)
def update_habit(
    habit_id: int,
    habit_update: HabitUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return update_user_habit(
        db=db, habit_id=habit_id, user_id=current_user.id, habit_update=habit_update
    )


@router.delete("/{habit_id}", status_code=204)
def delete_habit(
    habit_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)
):
    delete_user_habit(db=db, habit_id=habit_id, user_id=current_user.id)


# Habit Completion
@router.post(
    "/{habit_id}/complete", response_model=HabitCompletionRead, status_code=201
)
def complete_habit(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    habit_completion = mark_habit_complete(db=db, habit_id=habit_id, user_id=current_user.id)
    print(habit_completion)
    return habit_completion


@router.delete("/{habit_id}/complete/{completed_date}", status_code=204)
def delete_habit_completion(
    habit_id: int,
    completed_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    unmark_habit_complete(
        db=db, habit_id=habit_id, user_id=current_user.id, completed_date=completed_date
    )


@router.get("/{habit_id}/completions", response_model=list[HabitCompletionRead])
def habit_completions(
    habit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_habit_completion_history(
        db=db, habit_id=habit_id, user_id=current_user.id
    )


@router.get(
    "/{habit_id}/completed-on/{completed_date}",
    response_model=HabitCompletionStatusRead,
)
def habit_completed_status(
    habit_id: int,
    completed_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return HabitCompletionStatusRead(
        completed=habit_completed_on_date(
            db=db,
            habit_id=habit_id,
            user_id=current_user.id,
            completed_date=completed_date,
        )
    )
