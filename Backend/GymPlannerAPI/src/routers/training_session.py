from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Annotated

import src.crud.workout as training_service
import src.crud.training_session as training_session_service
import src.crud.set as exercise_in_session_service
from src.schemas.workout import TrainingSession, TrainingSessionBase
from src.schemas.user import User
from src.schemas.workout_exercise import ExerciseInSession
from src.core.dependencies import get_db, get_current_user

router = APIRouter(prefix="/training_sessions", tags=["Training session"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=TrainingSessionBase)
def create_training_session(current_user: Annotated[User, Depends(get_current_user)],
                            training_session_base: TrainingSessionBase, db: Session = Depends(get_db)):
    trainings = training_service.get_trainings_by_user_id(db, current_user.id)
    if not (training_session_base.training_id in [training.id for training in trainings]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to a training that you try to assign training session to."
        )

    return training_session_service.create_training_session(db, training_session_base)


@router.get("/{training_session_id}", response_model=TrainingSession)
def get_training_session(training_session_id: int, current_user: Annotated[
    User, Depends(get_current_user)],
                         db: Session = Depends(get_db)):
    session = training_session_service.get_training_session_by_id(db, training_session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Training session not found")

    trainings = training_service.get_trainings_by_user_id(db, current_user.id)
    if not (session.training_id in [training.id for training in trainings]):
        raise HTTPException(status_code=403, detail="You do not have access to a training session with given id")

    return session


@router.get("", response_model=list[TrainingSession])
def get_training_sessions(current_user: Annotated[User, Depends(get_current_user)],
                          db: Session = Depends(get_db)):
    return training_session_service.get_training_sessions_by_user_id(db, current_user.id)


@router.get("/{training_session_id}/exercises_in_session", response_model=list[ExerciseInSession])
def get_exercises_in_session(training_session_id: int, current_user: Annotated[User, Depends(get_current_user)],
                             db: Session = Depends(get_db)):
    training_session = training_session_service.get_training_session_by_id(db, training_session_id)
    if not training_session:
        raise HTTPException(status_code=404, detail="Session not found")

    trainings = training_service.get_trainings_by_user_id(db, current_user.id)
    if not (training_session.training_id in [training.id for training in trainings]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to a given session"
        )
    return exercise_in_session_service.get_exercises_in_session(db, training_session_id)
