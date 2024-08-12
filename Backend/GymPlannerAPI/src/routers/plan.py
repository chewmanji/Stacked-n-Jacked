from fastapi import APIRouter, Depends, HTTPException, status

import src.schemas.plan
import src.schemas.user
from src.core.dependencies import get_db, get_current_user
from src.core import crud
from src.core import schemas
from sqlalchemy.orm import Session
from typing import Annotated

router = APIRouter(prefix="/plans", tags=["Plan"])


@router.post("", status_code=status.HTTP_201_CREATED, response_model=src.schemas.plan.PlanBase)
def create_training(current_user: Annotated[src.schemas.user.User, Depends(get_current_user)],
                    plan_base: src.schemas.plan.PlanBase, db: Session = Depends(get_db)):
    plan = src.schemas.plan.PlanCreate(**plan_base.model_dump(), user_id=current_user.id)
    return crud.create_plan(db, plan)


@router.get("/{plan_id}", response_model=src.schemas.plan.Plan)
def get_plan(plan_id: int, current_user: Annotated[src.schemas.user.User, Depends(get_current_user)],
             db: Session = Depends(get_db)):
    plans = crud.get_plans_by_user_id(db, current_user.id)
    plan = next((plan for plan in plans if plan_id == plan.id), None)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    return plan


@router.get("", response_model=list[src.schemas.plan.Plan])
def get_plans(current_user: Annotated[src.schemas.user.User, Depends(get_current_user)], db: Session = Depends(get_db)):
    return crud.get_plans_by_user_id(db, current_user.id)


@router.patch("", response_model=src.schemas.plan.Plan)
def update_plan(current_user: Annotated[src.schemas.user.User, Depends(get_current_user)], plan_input: src.schemas.plan.PlanUpdate,
                db: Session = Depends(get_db)):
    plans = crud.get_plans_by_user_id(db, current_user.id)
    db_plan = next((pl for pl in plans if pl.id == plan_input.id), None)
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    model_plan = src.schemas.plan.Plan(**db_plan.__dict__)
    update_data = plan_input.dict(exclude_unset=True)
    updated_plan = model_plan.model_copy(update=update_data)
    return crud.update_plan(db, updated_plan)


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_plan(plan_id: int, current_user: Annotated[src.schemas.user.User, Depends(get_current_user)],
                db: Session = Depends(get_db)):
    plans = crud.get_plans_by_user_id(db, current_user.id)
    plan = next((pl for pl in plans if pl.id == plan_id), None)
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")

    crud.delete_plan(db, plan_id)
