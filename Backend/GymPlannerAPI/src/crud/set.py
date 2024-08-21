from typing import Type

from sqlalchemy.orm import Session

from src.models.set import Set as SetDB
from src.schemas.set import SetBase


def create_set(db: Session, ex_session_base: SetBase) -> SetDB:
    ex_db = SetDB(**ex_session_base.model_dump())
    db.add(ex_db)
    db.commit()
    db.refresh(ex_db)
    return ex_db


def get_set_in_session_by_id(db: Session, exercise_in_session_id: int) -> SetDB:
    return db.query(SetDB).get(exercise_in_session_id)


def get_sets_in_workout_exercise(db: Session, workout_exercise_id: int) -> list[Type[SetDB]]:
    return db.query(SetDB).filter(
        SetDB.workout_exercise_id == workout_exercise_id).all()


def get_sets_by_user_id(db: Session, user_id: int) -> list[Type[SetDB]]:
    return db.query(SetDB).filter(SetDB.user_id == user_id).all()
