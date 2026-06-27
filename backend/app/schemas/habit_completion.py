from datetime import date
from pydantic import BaseModel


class HabitCompletionRead(BaseModel):
    id: int
    habit_id: int
    completed_date: date

    model_config = {"from_attributes": True}

class HabitCompletionStatusRead(BaseModel):
    completed: bool
    