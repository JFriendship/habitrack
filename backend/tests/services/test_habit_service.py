import pytest

import app.services.habit_service as habit_service
from app.schemas.habit import HabitCreate, HabitUpdate

def test_create_habit_for_user_works(db_session, test_user):
    habit_name = "Exercise"
    habit_description = "30 minutes daily"
    habit = habit_service.create_habit_for_user(
        db=db_session, 
        habit_create=HabitCreate(name=habit_name, description=habit_description),
        user_id=test_user.id
    )

    assert habit.id is not None
    assert habit.name == habit_name
    assert habit.description == habit_description
    assert habit.user_id == test_user.id


def test_update_user_habit_works(db_session, test_user):
    habit = habit_service.create_habit_for_user(
        db=db_session, 
        habit_create=HabitCreate(name="Exercise", description="30 minutes daily"),
        user_id=test_user.id
    )
    update_name = "Drink Water"
    update_description = "2L Daily"
    updated_habit = habit_service.update_user_habit(
        db=db_session,
        habit_id=habit.id,
        user_id=test_user.id,
        habit_update=HabitUpdate(name=update_name, description=update_description),
    )

    assert updated_habit.id == habit.id
    assert updated_habit.name == update_name
    assert updated_habit.description == update_description
    assert updated_habit.user_id == test_user.id

def test_update_user_habit_breaks(db_session, test_user):
    update_name = "Drink Water"
    update_description = "2L Daily"
    with pytest.raises(Exception):
        updated_habit = habit_service.update_user_habit(
            db=db_session,
            habit_id=999,
            user_id=test_user.id,
            habit_update=HabitUpdate(name=update_name, description=update_description),
        )

def test_get_user_habits_works(db_session, test_user):
    habit = habit_service.create_habit_for_user(
        db=db_session, 
        habit_create=HabitCreate(name="Exercise", description="30 minutes daily"),
        user_id=test_user.id
    )

    habit_list = habit_service.get_user_habits(db=db_session, user_id=test_user.id)

    assert len(habit_list) == 1
    assert habit_list[0] == habit



def test_delete_user_habit_works(db_session, test_user):
    habit = habit_service.create_habit_for_user(
        db=db_session, 
        habit_create=HabitCreate(name="Exercise", description="30 minutes daily"),
        user_id=test_user.id
    )

    habit_service.delete_user_habit(db=db_session, habit_id=habit.id, user_id=test_user.id)

    habit_list = habit_service.get_user_habits(db=db_session, user_id=test_user.id)
    assert habit_list == []
