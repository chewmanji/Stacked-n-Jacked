from sqlalchemy.orm import Session

from src.models.user import User as UserDB
from src.schemas.user import UserCreate, UserUpdate
from src.core.security import get_password_hash
from sqlalchemy import update


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = UserDB(**user.model_dump(exclude={"password"}), hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int) -> UserDB | None:
    return db.query(UserDB).filter(UserDB.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> UserDB | None:
    return db.query(UserDB).filter(UserDB.email == email).first()


def update_user(db: Session, user_data: UserUpdate) -> UserDB | None:
    if user_data.password:
        hashed_password = get_password_hash(user_data.password)
        stmt = (update(UserDB)
                .where(UserDB.id == user_data.id)
                .values(**user_data.model_dump(exclude={"password"}), hashed_password=hashed_password)
                .returning(UserDB))
        res = db.execute(stmt).scalar_one_or_none()
        db.commit()
        return res

    stmt = (update(UserDB)
            .where(UserDB.id == user_data.id)
            .values(**user_data.model_dump(exclude_unset=True))
            .returning(UserDB))
    res = db.execute(stmt).scalar_one_or_none()
    db.commit()
    return res
