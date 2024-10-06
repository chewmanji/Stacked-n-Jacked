from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.orm import Session
from typing import Annotated

import src.crud.exercise as exercise_service
import src.crud.workout as workout_service
import src.crud.workout_exercise as workout_exercise_service
import src.crud.set as set_service
from src.schemas.user import User
from src.schemas.workout_exercise import WorkoutExercise, WorkoutExerciseBase, \
    WorkoutExerciseUpdate, WorkoutExerciseDetailsChart
from src.schemas.exercise import ExerciseBase
from src.schemas.set import Set
from src.core.dependencies import get_db, get_current_user

router = APIRouter(prefix="/workout_exercises", tags=["Workout Exercise"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=WorkoutExercise)
def create_workout_exercise(current_user: Annotated[User, Depends(get_current_user)],
                            workout_exercise_base: WorkoutExerciseBase, db: Session = Depends(get_db)):
    if not exercise_service.get_exercise_by_id(db, workout_exercise_base.exercise_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise with given id does not exist"
        )

    if workout_exercise_base.workout_id is not None and not (
            workout_exercise_base.workout_id in [workout.id for workout in
                                                 workout_service.get_workouts_by_user_id(db, current_user.id)]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to a workout that you try to assign exercise to."
        )

    return workout_exercise_service.create_workout_exercise(db, workout_exercise_base)


@router.get("", response_model=list[WorkoutExercise])
def get_workout_exercises(current_user: Annotated[User, Depends(get_current_user)],
                          db: Session = Depends(get_db)):
    return workout_exercise_service.get_workout_exercises_by_user_id(db, current_user.id)


@router.get("/exercises", response_model=list[ExerciseBase])
def get_exercises_from_workout_exercises(current_user: Annotated[User, Depends(get_current_user)],
                                         db: Session = Depends(get_db)):
    return workout_exercise_service.get_exercises_from_workout_exercises(db, current_user.id)


@router.get("/exercises/{id}", response_model=list[WorkoutExerciseDetailsChart], response_model_exclude_none=True)
def get_workout_exercises_by_exercise(current_user: Annotated[User, Depends(get_current_user)],
                                      id: Annotated[int, Path()],
                                      db: Session = Depends(get_db)):
    exs = workout_exercise_service.get_workout_exercises_by_exercise_id(db, current_user.id, id)
    result = [WorkoutExerciseDetailsChart(
        id=ex.id,
        sets=ex.sets,
        workout_date=ex.workout.workout_date,
    )
        for ex in exs]
    return result


@router.get("/{workout_exercise_id}", response_model=WorkoutExercise)
def get_workout_exercise(current_user: Annotated[User, Depends(get_current_user)],
                         workout_exercise_id: Annotated[int, Path()], db: Session = Depends(get_db)):
    workout_exercises = workout_exercise_service.get_workout_exercises_by_user_id(db, current_user.id)
    exercise = next((ex for ex in workout_exercises if ex.id == workout_exercise_id), None)
    if not exercise:
        raise HTTPException(status_code=404, detail="Workout exercise not found")
    return exercise


@router.get("/{workout_exercise_id}/sets", response_model=list[Set])
def get_sets_by_workout_exercise_id(current_user: Annotated[User, Depends(get_current_user)],
                                    workout_exercise_id: Annotated[int, Path()], db: Session = Depends(get_db)):
    workout_exercises = workout_exercise_service.get_workout_exercises_by_user_id(db, current_user.id)
    exercise = next((ex for ex in workout_exercises if ex.id == workout_exercise_id), None)

    if not exercise:
        raise HTTPException(status_code=404, detail="Workout exercise not found")

    return set_service.get_sets_in_workout_exercise(db, workout_exercise_id)


@router.patch("", response_model=WorkoutExercise)
def update_workout_exercise(current_user: Annotated[User, Depends(get_current_user)],
                            workout_exercise: WorkoutExerciseUpdate, db: Session = Depends(get_db)):
    workout_exercises = workout_exercise_service.get_workout_exercises_by_user_id(db, current_user.id)
    db_workout_exercise = next((ex for ex in workout_exercises if ex.id == workout_exercise.id), None)
    if not db_workout_exercise:
        raise HTTPException(status_code=404, detail="Workout exercise with given id does not exist")

    if (workout_exercise.exercise_id is not None and
            not exercise_service.get_exercise_by_id(db, workout_exercise.exercise_id)):
        raise HTTPException(
            status_code=404,
            detail="Exercise with given id does not exist"
        )

    model_workout_exercise = WorkoutExercise(**db_workout_exercise.__dict__)
    update_data = workout_exercise.dict(exclude_unset=True)
    updated_exercise = model_workout_exercise.model_copy(update=update_data)
    return workout_exercise_service.update_workout_exercise(db, updated_exercise)


@router.delete("/{workout_exercise_id}", status_code=204)
def delete_workout_exercise(current_user: Annotated[User, Depends(get_current_user)],
                            workout_exercise_id: int,
                            db: Session = Depends(get_db)):
    workout_exercises = workout_exercise_service.get_workout_exercises_by_user_id(db, current_user.id)
    workout_exercise_to_delete = next((ex for ex in workout_exercises if ex.id == workout_exercise_id), None)
    if not workout_exercise_to_delete:
        raise HTTPException(status_code=404, detail="Workout exercised with given id does not exist")

    workout_exercise_service.delete_workout_exercise(db, workout_exercise_id)
