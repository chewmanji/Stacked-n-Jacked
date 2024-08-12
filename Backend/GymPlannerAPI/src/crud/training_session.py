from typing import Type

from sqlalchemy.orm import Session

import src.models
import src.schemas


def create_training_session(db: Session, training_session: src.schemas.training.TrainingSessionBase) -> src.models.training.TrainingSession:
    session_db = src.models.training.TrainingSession(**training_session.model_dump())
    db.add(session_db)
    db.commit()
    db.refresh(session_db)
    return session_db


def get_training_session_by_id(db: Session, session_id: int) -> src.models.training.TrainingSession:
    return db.query(src.models.training.TrainingSession).get(session_id)


def get_training_sessions_by_user_id(db: Session, user_id: int) -> list[Type[src.models.training.TrainingSession]]:
    return (db.query(src.models.training.TrainingSession)
            .join(src.models.training.Training).join(src.models.user.User)
            .where(src.models.user.User.id == user_id)
            .all())
