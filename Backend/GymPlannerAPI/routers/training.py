from fastapi import APIRouter, Depends, HTTPException, status, Path
from core.dependencies import get_db, get_current_user
from core import schemas, crud
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(prefix="/trainings", tags=["Training"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.TrainingBase)
def create_training(current_user: Annotated[schemas.User, Depends(get_current_user)],
                    training_base: schemas.TrainingBase, db: Session = Depends(get_db)):
    plans = crud.get_plans_by_user_id(db, current_user.id)
    if training_base.plan_id is not None and not (training_base.plan_id not in [plan_id for plan_id in plans]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to a plan that you try to assign training to."
        )

    training = schemas.TrainingCreate(**training_base.model_dump(), user_id=current_user.id)
    return crud.create_training(db, training)


@router.get("/{training_id}", response_model=schemas.Training)
def get_training(training_id: int, current_user: Annotated[schemas.User, Depends(get_current_user)],
                 db: Session = Depends(get_db)):
    trainings = crud.get_trainings_by_user_id(db, current_user.id)
    training = next((training for training in trainings if training_id == training.id), None)
    if not training:
        raise HTTPException(status_code=404, detail="Training not found")

    return training


@router.get("", response_model=list[schemas.Training])
def get_trainings(current_user: Annotated[schemas.User, Depends(get_current_user)], db: Session = Depends(get_db)):
    return crud.get_trainings_by_user_id(db, current_user.id)


@router.patch("", response_model=schemas.Training)
def update_training(current_user: Annotated[schemas.User, Depends(get_current_user)],
                    training_input: schemas.TrainingUpdate,
                    db: Session = Depends(get_db)):
    trainings = crud.get_trainings_by_user_id(db, current_user.id)
    db_training = next((tr for tr in trainings if tr.id == training_input.id), None)
    if not db_training:
        raise HTTPException(status_code=404, detail="Training not found")

    plans = crud.get_plans_by_user_id(db, current_user.id)
    if training_input.plan_id is not None and not (training_input.plan_id in [plan.id for plan in plans]):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have access to a plan that you try to assign training to."
        )

    model_training = schemas.Training(**db_training.__dict__)
    update_data = training_input.dict(exclude_unset=True)
    updated_training = model_training.model_copy(update=update_data)
    return crud.update_training(db, updated_training)


@router.delete("/{training_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_training(training_id: int, current_user: Annotated[schemas.User, Depends(get_current_user)],
                    db: Session = Depends(get_db)):
    trainings = crud.get_trainings_by_user_id(db, current_user.id)
    training = next((tr for tr in trainings if tr.id == training_id), None)
    if not training:
        raise HTTPException(status_code=404, detail="Training not found")

    crud.delete_training(db, training_id)
