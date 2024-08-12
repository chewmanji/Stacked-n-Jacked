from fastapi import APIRouter, Depends, HTTPException, status, Path
from core.dependencies import get_db, get_current_user
from core import schemas, crud
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(prefix="/user_exercises", tags=["User Exercise"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.UserExerciseBase)
def create_user_exercise(current_user: Annotated[schemas.User, Depends(get_current_user)],
                         user_exercise_base: schemas.UserExerciseBase, db: Session = Depends(get_db)):
    if not crud.get_exercise_by_id(db, user_exercise_base.exercise_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exercise with given id does not exist"
        )

    if user_exercise_base.training_id is not None and not (
            user_exercise_base.training_id in [training.id for training in
                                               crud.get_trainings_by_user_id(db, current_user.id)]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to a training that you try to assign exercise to."
        )

    user_exercise = schemas.UserExerciseCreate(**user_exercise_base.model_dump(), user_id=current_user.id)
    return crud.create_user_exercise(db, user_exercise)


@router.get("/{user_exercise_id}", response_model=schemas.UserExercise)
def get_user_exercise(current_user: Annotated[schemas.User, Depends(get_current_user)],
                      user_exercise_id: Annotated[int, Path()], db: Session = Depends(get_db)):
    user_exercises = crud.get_user_exercises_by_user_id(db, current_user.id)
    exercise = next((ex for ex in user_exercises if ex.id == user_exercise_id), None)
    if not exercise:
        raise HTTPException(status_code=404, detail="User exercise not found")
    return exercise


@router.get("", response_model=list[schemas.UserExercise])
def get_user_exercises(current_user: Annotated[schemas.User, Depends(get_current_user)], db: Session = Depends(get_db)):
    return crud.get_user_exercises_by_user_id(db, current_user.id)


@router.patch("", response_model=schemas.UserExercise)
def update_user_exercise(current_user: Annotated[schemas.User, Depends(get_current_user)],
                         user_exercise: schemas.UserExerciseUpdate, db: Session = Depends(get_db)):
    user_exercises = crud.get_user_exercises_by_user_id(db, current_user.id)
    db_user_exercise = next((ex for ex in user_exercises if ex.id == user_exercise.id), None)
    if not db_user_exercise:
        raise HTTPException(status_code=404, detail="User exercise with given id does not exist")

    if user_exercise.exercise_id is not None and not crud.get_exercise_by_id(db, user_exercise.exercise_id):
        raise HTTPException(
            status_code=404,
            detail="Exercise with given id does not exist"
        )

    trainings = crud.get_trainings_by_user_id(db, current_user.id)
    if (user_exercise.training_id is not None) and not (
            user_exercise.training_id in [training.id for training in trainings]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to a training that you try to assign exercise to."
        )

    model_user_exercise = schemas.UserExercise(**db_user_exercise.__dict__)
    update_data = user_exercise.dict(exclude_unset=True)
    updated_exercise = model_user_exercise.model_copy(update=update_data)
    return crud.update_user_exercise(db, updated_exercise)


@router.delete("/{user_exercise_id}", status_code=204)
def delete_user_exercise(current_user: Annotated[schemas.User, Depends(get_current_user)], user_exercise_id: int,
                         db: Session = Depends(get_db)):
    user_exercises = crud.get_user_exercises_by_user_id(db, current_user.id)
    user_exercise_to_delete = next((ex for ex in user_exercises if ex.id == user_exercise_id), None)
    if not user_exercise_to_delete:
        raise HTTPException(status_code=404, detail="User exercise with given id does not exist")

    crud.delete_user_exercise(db, user_exercise_id)
