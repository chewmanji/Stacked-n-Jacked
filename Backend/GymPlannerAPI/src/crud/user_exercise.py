from typing import Type

from sqlalchemy import update
from sqlalchemy.orm import Session

from src.models.exercise import UserExercise as UserExerciseDB
from src.schemas.user_exercise import UserExercise, UserExerciseCreate


def create_user_exercise(db: Session, user_exercise: UserExerciseCreate) -> UserExerciseDB:
    user_exercise_db = UserExerciseDB(**user_exercise.model_dump())
    db.add(user_exercise_db)
    db.commit()
    db.refresh(user_exercise_db)
    return user_exercise_db


def get_user_exercise_by_id(db: Session, exercise_id: int) -> UserExerciseDB | None:
    return db.query(UserExerciseDB).get(exercise_id)


def get_user_exercises_by_user_id(db: Session, user_id: int) -> list[Type[UserExerciseDB]]:
    return db.query(UserExerciseDB).filter(UserExerciseDB.user_id == user_id).all()


def update_user_exercise(db: Session, user_exercise: UserExercise) -> UserExerciseDB | None:
    stmt = (update(UserExerciseDB)
            .where(UserExerciseDB.id == user_exercise.id)
            .values(**user_exercise.model_dump())
            .returning(UserExerciseDB))
    res = db.execute(stmt).scalar_one_or_none()
    db.commit()
    return res


def delete_user_exercise(db: Session, user_exercise_id: int) -> None:
    db_user_exercise = db.query(UserExerciseDB).get(user_exercise_id)
    db.delete(db_user_exercise)
    db.commit()
