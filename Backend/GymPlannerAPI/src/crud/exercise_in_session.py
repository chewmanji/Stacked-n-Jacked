from typing import Type

from sqlalchemy.orm import Session

import src.models
import src.schemas


def create_exercise_in_session(db: Session, ex_session_base: src.schemas.user_exercise.ExerciseInSessionBase) -> src.models.exercise.ExerciseInSession:
    ex_db = src.models.exercise.ExerciseInSession(**ex_session_base.model_dump())
    db.add(ex_db)
    db.commit()
    db.refresh(ex_db)
    return ex_db


def get_exercises_in_session(db: Session, session_id: int) -> list[Type[src.models.exercise.ExerciseInSession]]:
    return db.query(src.models.exercise.ExerciseInSession).filter(
        src.models.exercise.ExerciseInSession.training_session_id == session_id).all()
