from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Annotated

import src.crud.user as user_service
from src.schemas.user import User, UserCreate, UserUpdate
from src.core.schemas import Token
from src.core.security import create_access_token, ACCESS_TOKEN_EXPIRE_DAYS
from src.core.dependencies import get_db, get_current_user
from src.core.auth import authenticate_user

router = APIRouter(tags=["User"])


@router.get("/users/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.post("/users", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    return user_service.create_user(db=db, user=user)


@router.patch("/users", response_model=User | None)
def update_user(current_user: Annotated[User, Depends(get_current_user)], user_data: UserUpdate,
                db: Session = Depends(get_db)):
    user_with_email = user_service.get_user_by_email(db, email=user_data.email)
    if user_with_email and user_data.email != current_user.email:
        raise HTTPException(status_code=409, detail="Email already registered")

    model_user = UserUpdate(**current_user.dict())
    update_data = user_data.dict(exclude_unset=True)
    updated_user = model_user.model_copy(update=update_data)
    return user_service.update_user(db, updated_user)


@router.post("/token", response_model=Token)
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
    return Token(access_token=access_token, token_type="bearer")
# TODO should I invalidate JWT token after successful update???
