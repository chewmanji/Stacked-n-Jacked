from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session

from src.core.dependencies import get_db, get_current_user
from src.schemas.set import Set, SetBase
from src.schemas.user import User
import src.crud.set as set_service
import src.crud.workout_exercise as workout_exercise_service

router = APIRouter(prefix="/sets", tags=["Set"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=Set)
def create_set(current_user: Annotated[User, Depends(get_current_user)],
               set_base: SetBase, db: Session = Depends(get_db)):
    if not workout_exercise_service.get_workout_exercise_by_id(db, set_base.workout_exercise_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workout exercise with given id does not exist"
        )

    if not (set_base.workout_exercise_id
            in [workout_exercise.id for workout_exercise in
                workout_exercise_service.get_workout_exercises_by_user_id(db, current_user.id)]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to a workout exercise that you try to assign set to."
        )

    return set_service.create_set(db, set_base)


@router.get("", response_model=list[Set])
def get_sets(current_user: Annotated[User, Depends(get_current_user)],
                          db: Session = Depends(get_db)):
    return set_service.get_sets_by_user_id(db, current_user.id)

