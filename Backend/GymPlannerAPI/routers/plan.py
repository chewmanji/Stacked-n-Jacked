from fastapi import APIRouter, Depends, HTTPException, status, Path
from core.dependencies import get_db, get_current_user
from core import schemas, crud
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(prefix="/plans", tags=["Plan"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=schemas.PlanBase)
def create_training(current_user: Annotated[schemas.User, Depends(get_current_user)],
                    plan_base: schemas.PlanBase, db: Session = Depends(get_db)):
    plan = schemas.PlanCreate(**plan_base.model_dump(), user_id=current_user.id)
    return crud.create_plan(db, plan)


@router.get("/{plan_id}", response_model=schemas.Plan)
def get_plan(plan_id: int, current_user: Annotated[schemas.User, Depends(get_current_user)]):
    plan = next((plan for plan in current_user.plans if plan_id == plan.id), None)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    return plan


@router.get("", response_model=list[schemas.Plan])
def get_plans(current_user: Annotated[schemas.User, Depends(get_current_user)]):
    return current_user.plans


@router.patch("", response_model=schemas.Plan)
def update_plan(current_user: Annotated[schemas.User, Depends(get_current_user)], plan_input: schemas.PlanUpdate,
                db: Session = Depends(get_db)):
    plan = next((pl for pl in current_user.plans if pl.id == plan_input.id), None)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    update_data = plan_input.dict(exclude_unset=True)
    updated_plan = plan.model_copy(update=update_data)
    return crud.update_plan(db, updated_plan)


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plan(plan_id: int, current_user: Annotated[schemas.User, Depends(get_current_user)],
                db: Session = Depends(get_db)):
    plan = next((pl for pl in current_user.plans if pl.id == plan_id), None)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    crud.delete_plan(db, plan_id)
