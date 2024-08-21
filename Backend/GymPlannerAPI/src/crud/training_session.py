from typing import Type

from sqlalchemy.orm import Session

from src.models.training import TrainingSession as TrainingSessionDB, Training as TrainingDB
from src.models.user import User as UserDB
from src.schemas.workout import TrainingSessionBase


def create_training_session(db: Session, training_session: TrainingSessionBase) -> TrainingSessionDB:
    session_db = TrainingSessionDB(**training_session.model_dump())
    db.add(session_db)
    db.commit()
    db.refresh(session_db)
    return session_db


def get_training_session_by_id(db: Session, session_id: int) -> TrainingSessionDB:
    return db.query(TrainingSessionDB).get(session_id)


def get_training_sessions_by_user_id(db: Session, user_id: int) -> list[Type[TrainingSessionDB]]:
    return (db.query(TrainingSessionDB)
            .join(TrainingDB).join(UserDB)
            .where(UserDB.id == user_id)
            .all())


def get_training_sessions_by_training_id(db: Session, training_id: int) -> list[Type[TrainingSessionDB]]:
    return db.query(TrainingSessionDB).filter(TrainingSessionDB.training_id == training_id).all()
