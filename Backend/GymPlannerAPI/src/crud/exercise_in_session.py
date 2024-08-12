from typing import Type

from sqlalchemy.orm import Session

from src.models.exercise import ExerciseInSession as ExerciseInSessionDB
from src.schemas.user_exercise import ExerciseInSessionBase


def create_exercise_in_session(db: Session, ex_session_base: ExerciseInSessionBase) -> ExerciseInSessionDB:
    ex_db = ExerciseInSessionDB(**ex_session_base.model_dump())
    db.add(ex_db)
    db.commit()
    db.refresh(ex_db)
    return ex_db


def get_exercise_in_session_by_id(db: Session, exercise_in_session_id: int) -> ExerciseInSessionDB:
    return db.query(ExerciseInSessionDB).get(exercise_in_session_id)


def get_exercises_in_session(db: Session, session_id: int) -> list[Type[ExerciseInSessionDB]]:
    return db.query(ExerciseInSessionDB).filter(
        ExerciseInSessionDB.training_session_id == session_id).all()
