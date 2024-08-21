from typing import Type

from sqlalchemy import update
from sqlalchemy.orm import Session

from src.models.workout_exercise import WorkoutExercise as WorkoutExerciseDB
from src.schemas.workout_exercise import WorkoutExercise, WorkoutExerciseCreate


def create_workout_exercise(db: Session, workout_exercise: WorkoutExerciseCreate) -> WorkoutExerciseDB:
    workout_exercise_db = WorkoutExerciseDB(**workout_exercise.model_dump())
    db.add(workout_exercise_db)
    db.commit()
    db.refresh(workout_exercise_db)
    return workout_exercise_db


def get_workout_exercise_by_id(db: Session, exercise_id: int) -> WorkoutExerciseDB | None:
    return db.query(WorkoutExerciseDB).get(exercise_id)


def get_workout_exercises_by_workout_id(db: Session, workout_id: int) -> list[Type[WorkoutExerciseDB]]:
    return db.query(WorkoutExerciseDB).filter(WorkoutExerciseDB.workout_id == workout_id).all()


def get_workout_exercises_by_user_id(db: Session, user_id: int) -> list[Type[WorkoutExerciseDB]]:
    return db.query(WorkoutExerciseDB).filter(WorkoutExerciseDB.user_id == user_id).all()


def update_workout_exercise(db: Session, workout_exercise: WorkoutExercise) -> WorkoutExerciseDB | None:
    stmt = (update(WorkoutExerciseDB)
            .where(WorkoutExerciseDB.id == workout_exercise.id)
            .values(**workout_exercise.model_dump())
            .returning(WorkoutExerciseDB))
    res = db.execute(stmt).scalar_one_or_none()
    db.commit()
    return res


def delete_workout_exercise(db: Session, workout_exercise_id: int) -> None:
    db_workout_exercise = db.query(WorkoutExerciseDB).get(workout_exercise_id)
    db.delete(db_workout_exercise)
    db.commit()
