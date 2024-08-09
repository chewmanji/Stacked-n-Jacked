from fastapi import APIRouter, Depends, HTTPException, status, Path
from core.dependencies import get_db, get_current_user
from core import schemas, crud
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(prefix="/exercises_in_session", tags=["Exercise in session"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.ExerciseInSession)
def create_exercise_in_session(current_user: Annotated[schemas.User, Depends(get_current_user)],
                               ex_session_base: schemas.ExerciseInSessionBase, db: Session = Depends(get_db)):
    if not current_user.has_access_to_user_exercise(ex_session_base.user_exercise_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to a exercise that you try to assign exercise in session to."
        )

    return crud.create_exercise_in_session(db, ex_session_base)


@router.get("/{session_id}", status_code=status.HTTP_200_OK, response_model=list[schemas.ExerciseInSession])
def get_exercises_in_session(session_id: int, current_user: Annotated[schemas.User, Depends(get_current_user)],
                             db: Session = Depends(get_db)):
    training_session = crud.get_training_session_by_id(db, session_id)
    if not training_session:
        raise HTTPException(status_code=404, detail="Session not found")

    if not current_user.has_access_to_training(training_session.training_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to a given session"
        )
    return crud.get_exercises_in_session(db, session_id)
