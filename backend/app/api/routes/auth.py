from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate, UserRead
from app.db.dependencies import get_db
from app.services.user_service import register_user, authenticate_user, EmailDoesNotExistError
from app.schemas.auth import Token
from app.core.security import create_access_token
from app.api.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post(path="/register", response_model=UserRead, status_code=201)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(db=db, user_create=user)

@router.post(path="/login", response_model=Token)
def login(login_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    try:
        user = authenticate_user(db=db, email=login_data.username, password=login_data.password)
        if user is None:
            raise HTTPException(
                status_code=401,
                detail="Incorrect Password"
            )
        
        access_token = create_access_token(str(user.id))

        return Token(access_token=access_token, token_type="bearer")

    except EmailDoesNotExistError:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email"
        )
    
@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return current_user