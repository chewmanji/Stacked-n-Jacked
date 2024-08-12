from typing import Type

from sqlalchemy import update
from sqlalchemy.orm import Session

import src.models
import src.schemas


def create_user_exercise(db: Session, user_exercise: src.schemas.user_exercise.UserExerciseCreate) -> src.models.exercise.UserExercise:
    user_exercise_db = src.models.exercise.UserExercise(**user_exercise.model_dump())
    db.add(user_exercise_db)
    db.commit()
    db.refresh(user_exercise_db)
    return user_exercise_db


def get_user_exercise_by_id(db: Session, exercise_id: int) -> src.models.exercise.UserExercise | None:
    return db.query(src.models.exercise.UserExercise).get(exercise_id)


def get_user_exercises_by_user_id(db: Session, user_id: int) -> list[Type[src.models.exercise.UserExercise]]:
    return db.query(src.models.exercise.UserExercise).filter(src.models.exercise.UserExercise.user_id == user_id).all()


def update_user_exercise(db: Session, user_exercise: src.schemas.user_exercise.UserExercise) -> src.models.exercise.UserExercise | None:
    stmt = (update(src.models.exercise.UserExercise)
            .where(src.models.exercise.UserExercise.id == user_exercise.id)
            .values(**user_exercise.model_dump())
            .returning(src.models.exercise.UserExercise))
    res = db.execute(stmt).scalar_one_or_none()
    db.commit()
    return res


def delete_user_exercise(db: Session, user_exercise_id: int) -> None:
    db_user_exercise = db.query(src.models.exercise.UserExercise).get(user_exercise_id)
    db.delete(db_user_exercise)
    db.commit()
