from typing import Type

from sqlalchemy import update
from sqlalchemy.orm import Session

import src.models
import src.schemas


def create_training(db: Session, training: src.schemas.training.TrainingCreate) -> src.models.training.Training | None:
    training_db = src.models.training.Training(**training.model_dump())
    db.add(training_db)
    db.commit()
    db.refresh(training_db)
    return training_db


def update_training(db: Session, updated_training: src.schemas.training.Training) -> src.models.training.Training | None:
    stmt = (update(src.models.training.Training)
            .where(src.models.training.Training.id == updated_training.id)
            .values(**updated_training.model_dump())
            .returning(src.models.training.Training))

    res = db.execute(stmt).scalar_one_or_none()
    db.commit()
    return res


def delete_training(db: Session, training_id: int) -> None:
    training_db = db.query(src.models.training.Training).get(training_id)
    db.delete(training_db)
    db.commit()


def get_trainings_by_user_id(db: Session, user_id:int) -> list[Type[src.models.training.Training]]:
    return db.query(src.models.training.Training).filter(src.models.training.Training.user_id == user_id).all()
