from typing import Type

from sqlalchemy import update
from sqlalchemy.orm import Session

import src.models
import src.schemas


def create_plan(db: Session, plan: src.schemas.plan.PlanCreate) -> src.models.plan.Plan:
    plan_db = src.models.plan.Plan(**plan.model_dump())
    db.add(plan_db)
    db.commit()
    db.refresh(plan_db)
    return plan_db


def update_plan(db: Session, updated_plan: src.schemas.plan.Plan) -> src.models.plan.Plan:
    stmt = (update(src.models.plan.Plan)
            .where(src.models.plan.Plan.id == updated_plan.id)
            .values(**updated_plan.model_dump())
            .returning(src.models.plan.Plan))

    res = db.execute(stmt).scalar_one_or_none()
    db.commit()
    return res


def delete_plan(db: Session, plan_id: int) -> None:
    plan_db = db.query(src.models.plan.Plan).get(plan_id)
    db.delete(plan_db)
    db.commit()


def get_plans_by_user_id(db:Session, user_id: int) -> list[Type[src.models.plan.Plan]]:
    return db.query(src.models.plan.Plan).filter(src.models.plan.Plan.user_id == user_id).all()
