from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy import update

import src.models.exercise
import src.models.plan
import src.models.training
import src.models.user
import src.schemas.plan
import src.schemas.training
import src.schemas.user
import src.schemas.user_exercise
from src.core.security import get_password_hash
from src.core import models, schemas


def create_user(db: Session, user: src.schemas.user.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = src.models.user.User(**user.model_dump(exclude={"password"}), hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int) -> src.models.user.User | None:
    return db.query(src.models.user.User).filter(src.models.user.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> src.models.user.User | None:
    return db.query(src.models.user.User).filter(src.models.user.User.email == email).first()


def get_exercises(db: Session, skip: int = 0, limit: int = 50) -> list[Type[src.models.exercise.Exercise]]:
    return db.query(src.models.exercise.Exercise).offset(skip).limit(limit).all()


def get_exercise_by_id(db: Session, exercise_id: int) -> src.models.exercise.Exercise | None:
    return db.query(src.models.exercise.Exercise).get(exercise_id)


def create_user_exercise(db: Session, user_exercise: src.schemas.user_exercise.UserExerciseCreate) -> src.models.exercise.UserExercise:
    user_exercise_db = src.models.exercise.UserExercise(**user_exercise.model_dump())
    db.add(user_exercise_db)
    db.commit()
    db.refresh(user_exercise_db)
    return user_exercise_db


def get_user_exercise_by_id(db: Session, exercise_id: int) -> src.models.exercise.UserExercise | None:
    return db.query(src.models.exercise.UserExercise).get(exercise_id)


def get_user_exercises_by_user_id(db: Session, user_id: int) -> list[Type[src.models.exercise.UserExercise]]:
    return db.query(src.models.exercise.UserExercise).filter(src.models.exercise.UserExercise.user_id == user_id).all()


def update_user_exercise(db: Session, user_exercise: src.schemas.user_exercise.UserExercise) -> src.models.exercise.UserExercise | None:
    stmt = (update(src.models.exercise.UserExercise)
            .where(src.models.exercise.UserExercise.id == user_exercise.id)
            .values(**user_exercise.model_dump())
            .returning(src.models.exercise.UserExercise))
    res = db.execute(stmt).scalar_one_or_none()
    db.commit()
    return res


def delete_user_exercise(db: Session, user_exercise_id: int) -> None:
    db_user_exercise = db.query(src.models.exercise.UserExercise).get(user_exercise_id)
    db.delete(db_user_exercise)
    db.commit()


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


def create_exercise_in_session(db: Session, ex_session_base: src.schemas.user_exercise.ExerciseInSessionBase) -> src.models.exercise.ExerciseInSession:
    ex_db = src.models.exercise.ExerciseInSession(**ex_session_base.model_dump())
    db.add(ex_db)
    db.commit()
    db.refresh(ex_db)
    return ex_db


def get_exercises_in_session(db: Session, session_id: int) -> list[Type[src.models.exercise.ExerciseInSession]]:
    return db.query(src.models.exercise.ExerciseInSession).filter(
        src.models.exercise.ExerciseInSession.training_session_id == session_id).all()
