from fastapi import APIRouter, Depends, HTTPException, status
from typing import Annotated
from sqlalchemy.orm import Session

import src.crud.exercise_in_session as ex_in_session_service
import src.crud.training_session as training_session_service
import src.crud.user_exercise as user_exercise_service
import src.crud.training as training_service
from src.schemas.user import User
from src.schemas.user_exercise import ExerciseInSessionBase, ExerciseInSession
from src.core.dependencies import get_db, get_current_user

router = APIRouter(prefix="/exercises_in_session", tags=["Exercise in session"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=ExerciseInSession)
def create_exercise_in_session(current_user: Annotated[User, Depends(get_current_user)],
                               ex_session_base: ExerciseInSessionBase,
                               db: Session = Depends(get_db)):
    user_exercises = user_exercise_service.get_user_exercises_by_user_id(db, current_user.id)
    if not (ex_session_base.user_exercise_id in [user_exercise.id for user_exercise in user_exercises]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to a exercise that you try to assign exercise in session to."
        )

    return ex_in_session_service.create_exercise_in_session(db, ex_session_base)


@router.get("/{session_id}", status_code=status.HTTP_200_OK, response_model=list[
    ExerciseInSession])
def get_exercises_in_session(session_id: int, current_user: Annotated[User, Depends(get_current_user)],
                             db: Session = Depends(get_db)):
    training_session = training_session_service.get_training_session_by_id(db, session_id)
    if not training_session:
        raise HTTPException(status_code=404, detail="Session not found")

    trainings = training_service.get_trainings_by_user_id(db, current_user.id)
    if not (training_session.training_id in [training.id for training in trainings]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to a given session"
        )
    return ex_in_session_service.get_exercises_in_session(db, session_id)
