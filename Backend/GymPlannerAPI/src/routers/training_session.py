from fastapi import APIRouter, Depends, HTTPException, status

import src.crud.training
import src.crud.training_session
import src.schemas.training
import src.schemas.user
from src.core.dependencies import get_db, get_current_user
from src.core import crud
from src.core import schemas
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(prefix="/training_sessions", tags=["Training session"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=src.schemas.training.TrainingSessionBase)
def create_training_session(current_user: Annotated[src.schemas.user.User, Depends(get_current_user)],
                            training_session_base: src.schemas.training.TrainingSessionBase, db: Session = Depends(get_db)):
    trainings = src.crud.training.get_trainings_by_user_id(db, current_user.id)
    if not (training_session_base.training_id in [training.id for training in trainings]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to a training that you try to assign training session to."
        )

    return src.crud.training_session.create_training_session(db, training_session_base)


@router.get("/{training_session_id}", response_model=src.schemas.training.TrainingSession)
def get_training_session(training_session_id: int, current_user: Annotated[
    src.schemas.user.User, Depends(get_current_user)],
                         db: Session = Depends(get_db)):
    session = src.crud.training_session.get_training_session_by_id(db, training_session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Training session not found")

    trainings = src.crud.training.get_trainings_by_user_id(db, current_user.id)
    if not (session.training_id in [training.id for training in trainings]):
        raise HTTPException(status_code=403, detail="You do not have access to a training session with given id")

    return session


@router.get("", response_model=list[src.schemas.training.TrainingSession])
def get_training_sessions(current_user: Annotated[src.schemas.user.User, Depends(get_current_user)],
                          db: Session = Depends(get_db)):
    return src.crud.training_session.get_training_sessions_by_user_id(db, current_user.id)


