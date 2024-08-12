from typing import Type

from sqlalchemy.orm import Session

from src.models.exercise import Exercise as ExerciseDB


def get_exercises(db: Session, skip: int = 0, limit: int = 50) -> list[Type[ExerciseDB]]:
    return db.query(ExerciseDB).offset(skip).limit(limit).all()


def get_exercise_by_id(db: Session, exercise_id: int) -> ExerciseDB | None:
    return db.query(ExerciseDB).get(exercise_id)
