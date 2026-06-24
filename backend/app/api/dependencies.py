from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.repositories.user_repository import get_user_by_id
from app.db.dependencies import get_db
from app.core.security import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_access_token(token)
        print(payload)
        user_id = int(payload["sub"])
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )
    user = get_user_by_id(db, user_id)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication credentials"
        )
    
    return user