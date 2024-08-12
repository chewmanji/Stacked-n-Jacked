from typing import Type

from sqlalchemy.orm import Session

import src.models


def get_exercises(db: Session, skip: int = 0, limit: int = 50) -> list[Type[src.models.exercise.Exercise]]:
    return db.query(src.models.exercise.Exercise).offset(skip).limit(limit).all()


def get_exercise_by_id(db: Session, exercise_id: int) -> src.models.exercise.Exercise | None:
    return db.query(src.models.exercise.Exercise).get(exercise_id)
