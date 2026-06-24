from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.habit import HabitCreate, HabitRead, HabitUpdate
from app.services.habit_service import create_habit_for_user, get_user_habits, update_user_habit, delete_user_habit

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
