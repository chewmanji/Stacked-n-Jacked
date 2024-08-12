from typing import Type

from sqlalchemy import update
from sqlalchemy.orm import Session

from src.models.plan import Plan as PlanDB
from src.schemas.plan import PlanCreate, Plan


def create_plan(db: Session, plan: PlanCreate) -> PlanDB:
    plan_db = PlanDB(**plan.model_dump())
    db.add(plan_db)
    db.commit()
    db.refresh(plan_db)
    return plan_db


def update_plan(db: Session, updated_plan: Plan) -> PlanDB:
    stmt = (update(PlanDB)
            .where(PlanDB.id == updated_plan.id)
            .values(**updated_plan.model_dump())
            .returning(PlanDB))

    res = db.execute(stmt).scalar_one_or_none()
    db.commit()
    return res


def delete_plan(db: Session, plan_id: int) -> None:
    plan_db = db.query(PlanDB).get(plan_id)
    db.delete(plan_db)
    db.commit()


def get_plans_by_user_id(db: Session, user_id: int) -> list[Type[PlanDB]]:
    return db.query(PlanDB).filter(PlanDB.user_id == user_id).all()
