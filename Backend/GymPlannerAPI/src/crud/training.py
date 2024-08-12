from typing import Type

from sqlalchemy import update
from sqlalchemy.orm import Session

from src.models.training import Training as TrainingDB
from src.schemas.training import TrainingCreate, Training


def create_training(db: Session, training: TrainingCreate) -> TrainingDB | None:
    training_db = TrainingDB(**training.model_dump())
    db.add(training_db)
    db.commit()
    db.refresh(training_db)
    return training_db


def update_training(db: Session, updated_training: Training) -> TrainingDB | None:
    stmt = (update(TrainingDB)
            .where(TrainingDB.id == updated_training.id)
            .values(**updated_training.model_dump())
            .returning(TrainingDB))

    res = db.execute(stmt).scalar_one_or_none()
    db.commit()
    return res


def delete_training(db: Session, training_id: int) -> None:
    training_db = db.query(TrainingDB).get(training_id)
    db.delete(training_db)
    db.commit()


def get_trainings_by_user_id(db: Session, user_id: int) -> list[Type[TrainingDB]]:
    return db.query(TrainingDB).filter(TrainingDB.user_id == user_id).all()
