from core.database import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from core import schemas, models, crud
from core.security import SECRET_KEY, ALGORITHM
import jwt
from typing import Annotated
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> schemas.User:
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
    user = crud.get_user_by_id(db, user_id=token_data.user_id)
    if user is None:
        raise credentials_exception
    return schemas.User.model_validate(user)
