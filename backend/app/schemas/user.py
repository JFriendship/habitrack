from pydantic import BaseModel, Field, EmailStr
import app.core.constants as const

class UserCreate(BaseModel):
    username: str = Field(..., min_length=const.MIN_USERNAME_LENGTH, max_length=const.MAX_USERNAME_LENGTH)
    email: EmailStr
    password: str = Field(..., min_length=const.MIN_PASSWORD_LENGTH, max_length=const.MAX_PASSWORD_LENGTH)

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
