from typing import Type

from sqlalchemy import update
from sqlalchemy.orm import Session

from src.models.workout_exercise import WorkoutExercise as WorkoutExerciseDB
from src.models.workout import Workout as WorkoutDB
from src.models.exercise import Exercise as ExerciseDB
from src.schemas.workout_exercise import WorkoutExercise, WorkoutExerciseBase


def create_workout_exercise(db: Session, workout_exercise: WorkoutExerciseBase) -> WorkoutExerciseDB:
    workout_exercise_db = WorkoutExerciseDB(**workout_exercise.model_dump())
    db.add(workout_exercise_db)
    db.commit()
    db.refresh(workout_exercise_db)
    return workout_exercise_db


def get_workout_exercise_by_id(db: Session, exercise_id: int) -> WorkoutExerciseDB | None:
    return db.query(WorkoutExerciseDB).get(exercise_id)


def get_workout_exercises_by_workout_id(db: Session, workout_id: int) -> list[Type[WorkoutExerciseDB]]:
    return (db.query(WorkoutExerciseDB)
            .filter(WorkoutExerciseDB.workout_id == workout_id)
            .all())


def get_workout_exercises_by_user_id(db: Session, user_id: int) -> list[Type[WorkoutExerciseDB]]:
    return (db.query(WorkoutExerciseDB)
            .join(WorkoutExerciseDB.workout)
            .where(WorkoutDB.user_id == user_id)
            .all())


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


def get_exercises_from_workout_exercises(db: Session, user_id: int) -> list[Type[ExerciseDB]]:
    return (db.query(ExerciseDB)
            .join(WorkoutExerciseDB)
            .join(WorkoutDB)
            .where(WorkoutDB.user_id == user_id)
            .all())


def get_workout_exercises_by_exercise_id(db: Session, user_id: int, exercise_id: int) -> list[Type[WorkoutExerciseDB]]:
    return (db.query(WorkoutExerciseDB)
            .join(ExerciseDB)
            .where(ExerciseDB.id == exercise_id)
            .join(WorkoutDB)
            .where(WorkoutDB.user_id == user_id)
            .all())


def get_latest_exercises(db: Session, user_id: int)->list[Type[WorkoutExerciseDB]]:
    return (db.query(WorkoutExerciseDB)
            .join(ExerciseDB)
            .join(WorkoutDB)
            .where(WorkoutDB.user_id == user_id)
            .all())