from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated

import src.schemas.user
from src.core import crud
from src.core import schemas
from src.core.security import create_access_token, ACCESS_TOKEN_EXPIRE_DAYS
from src.core.dependencies import get_db, get_current_user
from src.core.auth import authenticate_user

router = APIRouter(tags=["User"])


@router.get("/users/me", response_model=src.schemas.user.User)
async def read_users_me(current_user: Annotated[src.schemas.user.User, Depends(get_current_user)]):
    return current_user


@router.post("/users", response_model=src.schemas.user.User)
def create_user(user: src.schemas.user.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@router.post("/token", response_model=schemas.Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")
