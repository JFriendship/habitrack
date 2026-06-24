from pydantic import BaseModel, Field
import app.core.constants as const

class HabitCreate(BaseModel):
    name: str = Field(min_length=const.MIN_HABIT_NAME_LENGTH, max_length=const.MAX_HABIT_NAME_LENGTH)
    description: str = Field(default=None, max_length=const.MAX_HABIT_DESCRIPTION_LENGTH)

class HabitRead(BaseModel):
    id: int
    name: str
    description: str | None
    user_id: int

    model_config = {
        "from_attributes": True
    }

class HabitUpdate(BaseModel):
    name: str = Field(min_length=const.MIN_HABIT_NAME_LENGTH, max_length=const.MAX_HABIT_NAME_LENGTH)
    description: str = Field(default=None, max_length=const.MAX_HABIT_DESCRIPTION_LENGTH)