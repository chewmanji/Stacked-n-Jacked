from typing import Type

from sqlalchemy import update
from sqlalchemy.orm import Session

from src.models.workout import Workout as WorkoutDB
from src.schemas.workout import WorkoutCreate, Workout


def create_workout(db: Session, workout: WorkoutCreate) -> WorkoutDB | None:
    workout_db = WorkoutDB(**workout.model_dump())
    db.add(workout_db)
    db.commit()
    db.refresh(workout_db)
    return workout_db


def update_workout(db: Session, updated_workout: Workout) -> WorkoutDB | None:
    stmt = (update(WorkoutDB)
            .where(WorkoutDB.id == updated_workout.id)
            .values(**updated_workout.model_dump())
            .returning(WorkoutDB))

    res = db.execute(stmt).scalar_one_or_none()
    db.commit()
    return res


def delete_workout(db: Session, workout_id: int) -> None:
    workout_db = db.query(WorkoutDB).get(workout_id)
    db.delete(workout_db)
    db.commit()


def get_workouts_by_user_id(db: Session, user_id: int) -> list[Type[WorkoutDB]]:
    return db.query(WorkoutDB).filter(WorkoutDB.user_id == user_id).all()
