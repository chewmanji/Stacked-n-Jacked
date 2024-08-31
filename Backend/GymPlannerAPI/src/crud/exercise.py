from typing import Type

from sqlalchemy.orm import Session

from src.models.exercise import Exercise as ExerciseDB
from src.models.workout import Workout as WorkoutDB
from src.models.workout_exercise import WorkoutExercise as WorkoutExerciseDB
from src.models.set import Set as SetDB


def get_exercises(db: Session, skip: int = 0, limit: int = 50) -> list[Type[ExerciseDB]]:
    return db.query(ExerciseDB).offset(skip).limit(limit).all()


def get_exercise_by_id(db: Session, exercise_id: int) -> ExerciseDB | None:
    return db.query(ExerciseDB).get(exercise_id)


def get_exercise_sets_by_user_id(db, exercise_id, user_id) -> list[SetDB]:
    return (db.query(SetDB)
            .join(SetDB.workout_exercise)
            .join(WorkoutExerciseDB.workout)
            .where(WorkoutDB.user_id == user_id, WorkoutExerciseDB.exercise_id == exercise_id)
            .all())
