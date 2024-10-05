from typing import Type

from sqlalchemy import update
from sqlalchemy.orm import Session

from src.models.workout import Workout as WorkoutDB
from src.models.workout_exercise import WorkoutExercise as WorkoutExerciseDB
from src.models.set import Set as SetDB
from src.schemas.workout import WorkoutCreate, Workout


def create_workout(db: Session, workout: WorkoutCreate) -> WorkoutDB | None:
    #TODO do refactoru? wydzielić do osobnych funckji to co jest w forach
    workout_db = WorkoutDB(
        type=workout.type,
        notes=workout.notes,
        user_id=workout.user_id
    )
    db.add(workout_db)
    db.commit()
    for workout_ex in workout.workout_exercises:
        workout_ex_db = WorkoutExerciseDB(
            exercise_id=workout_ex.exercise_id,
            workout_id=workout_db.id
        )
        db.add(workout_ex_db)
        db.commit()
        for set in workout_ex.sets:
            set_db = SetDB(
                reps_count=set.reps_count,
                weight=set.weight,
                set_number=set.set_number,
                workout_exercise_id=workout_ex_db.id
            )
            db.add(set_db)
            db.commit()

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
