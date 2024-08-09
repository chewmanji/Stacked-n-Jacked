from fastapi import APIRouter, Depends, HTTPException, status, Path
from core.dependencies import get_db, get_current_user
from core import schemas, crud
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(prefix="/training_sessions", tags=["Training session"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.TrainingSessionBase)
def create_training_session(current_user: Annotated[schemas.User, Depends(get_current_user)],
                            training_session_base: schemas.TrainingSessionBase, db: Session = Depends(get_db)):
    if not current_user.has_access_to_training(training_session_base.training_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to a training that you try to assign training session to."
        )

    return crud.create_training_session(db, training_session_base)


@router.get("/{training_session_id}", response_model=schemas.TrainingSession)
def get_training_session(training_session_id: int, current_user: Annotated[schemas.User, Depends(get_current_user)],
                         db: Session = Depends(get_db)):
    session = crud.get_training_session_by_id(db, training_session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Training session not found")

    if not current_user.has_access_to_training(session.training_id):
        raise HTTPException(status_code=403, detail="You do not have access to a training session with given id")

    return session


@router.get("", response_model=list[schemas.TrainingSession])
def get_training_sessions(current_user: Annotated[schemas.User, Depends(get_current_user)],
                          db: Session = Depends(get_db)):
    return crud.get_training_sessions_by_user_id(db, current_user.id)


