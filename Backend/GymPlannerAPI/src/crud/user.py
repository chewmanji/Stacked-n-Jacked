from sqlalchemy.orm import Session

import src.models
import src.schemas
from src.core.security import get_password_hash


def create_user(db: Session, user: src.schemas.user.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = src.models.user.User(**user.model_dump(exclude={"password"}), hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int) -> src.models.user.User | None:
    return db.query(src.models.user.User).filter(src.models.user.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> src.models.user.User | None:
    return db.query(src.models.user.User).filter(src.models.user.User.email == email).first()
