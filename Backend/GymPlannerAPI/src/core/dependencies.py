from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session
import jwt
from jwt.exceptions import InvalidTokenError

import src.crud.user
import src.schemas.user
from src.core.database import SessionLocal
from src.core import schemas
from src.core.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                     db: Session = Depends(get_db)) -> src.schemas.user.User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise credentials_exception
        token_data = schemas.TokenData(user_id=user_id)
    except InvalidTokenError:
        raise credentials_exception
    user = src.crud.user.get_user_by_id(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return src.schemas.user.User.model_validate(user)

