from sqlalchemy.orm import Session
from fastapi import Depends
from core.dependencies import get_db
from core import crud
from core.security import verify_password


def authenticate_user(username: str, password: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
