from fastapi import APIRouter, Depends, HTTPException, status

import src.crud.exercise_in_session
import src.crud.training
import src.crud.training_session
import src.crud.user_exercise
import src.schemas.user
import src.schemas.user_exercise
from src.core.dependencies import get_db, get_current_user
from src.core import crud
from src.core import schemas
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(prefix="/exercises_in_session", tags=["Exercise in session"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=src.schemas.user_exercise.ExerciseInSession)
def create_exercise_in_session(current_user: Annotated[src.schemas.user.User, Depends(get_current_user)],
                               ex_session_base: src.schemas.user_exercise.ExerciseInSessionBase, db: Session = Depends(get_db)):
    user_exercises = src.crud.user_exercise.get_user_exercises_by_user_id(db, current_user.id)
    if not (ex_session_base.user_exercise_id in [user_exercise.id for user_exercise in user_exercises]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to a exercise that you try to assign exercise in session to."
        )

    return src.crud.exercise_in_session.create_exercise_in_session(db, ex_session_base)


@router.get("/{session_id}", status_code=status.HTTP_200_OK, response_model=list[
    src.schemas.user_exercise.ExerciseInSession])
def get_exercises_in_session(session_id: int, current_user: Annotated[src.schemas.user.User, Depends(get_current_user)],
                             db: Session = Depends(get_db)):
    training_session = src.crud.training_session.get_training_session_by_id(db, session_id)
    if not training_session:
        raise HTTPException(status_code=404, detail="Session not found")

    trainings = src.crud.training.get_trainings_by_user_id(db, current_user.id)
    if not (training_session.training_id in [training.id for training in trainings]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to a given session"
        )
    return src.crud.exercise_in_session.get_exercises_in_session(db, session_id)
