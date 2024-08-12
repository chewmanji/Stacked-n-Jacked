from typing import Type

from sqlalchemy.orm import Session
from sqlalchemy import update, delete
from core.security import get_password_hash
from core import models, schemas


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(**user.model_dump(exclude={"password"}), hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> models.User | None:
    return db.query(models.User).filter(models.User.email == email).first()


def get_exercises(db: Session, skip: int = 0, limit: int = 50) -> list[Type[models.Exercise]]:
    return db.query(models.Exercise).offset(skip).limit(limit).all()


def get_exercise_by_id(db: Session, exercise_id: int) -> models.Exercise | None:
    return db.query(models.Exercise).get(exercise_id)


def create_user_exercise(db: Session, user_exercise: schemas.UserExerciseCreate) -> models.UserExercise:
    user_exercise_db = models.UserExercise(**user_exercise.model_dump())
    db.add(user_exercise_db)
    db.commit()
    db.refresh(user_exercise_db)
    return user_exercise_db


def get_user_exercise_by_id(db: Session, exercise_id: int) -> models.UserExercise | None:
    return db.query(models.UserExercise).get(exercise_id)


def get_user_exercises_by_user_id(db: Session, user_id: int) -> list[Type[models.UserExercise]]:
    return db.query(models.UserExercise).filter(models.UserExercise.user_id == user_id).all()


def update_user_exercise(db: Session, user_exercise: schemas.UserExercise) -> models.UserExercise | None:
    stmt = (update(models.UserExercise)
            .where(models.UserExercise.id == user_exercise.id)
            .values(**user_exercise.model_dump())
            .returning(models.UserExercise))
    res = db.execute(stmt).scalar_one_or_none()
    db.commit()
    return res


def delete_user_exercise(db: Session, user_exercise_id: int) -> None:
    db_user_exercise = db.query(models.UserExercise).get(user_exercise_id)
    db.delete(db_user_exercise)
    db.commit()


def create_training(db: Session, training: schemas.TrainingCreate) -> models.Training | None:
    training_db = models.Training(**training.model_dump())
    db.add(training_db)
    db.commit()
    db.refresh(training_db)
    return training_db


def update_training(db: Session, updated_training: schemas.Training) -> models.Training | None:
    stmt = (update(models.Training)
            .where(models.Training.id == updated_training.id)
            .values(**updated_training.model_dump())
            .returning(models.Training))

    res = db.execute(stmt).scalar_one_or_none()
    db.commit()
    return res


def delete_training(db: Session, training_id: int) -> None:
    training_db = db.query(models.Training).get(training_id)
    db.delete(training_db)
    db.commit()

def get_trainings_by_user_id(db: Session, user_id:int) -> list[Type[models.Training]]:
    return db.query(models.Training).filter(models.Training.user_id == user_id).all()


def create_plan(db: Session, plan: schemas.PlanCreate) -> models.Plan:
    plan_db = models.Plan(**plan.model_dump())
    db.add(plan_db)
    db.commit()
    db.refresh(plan_db)
    return plan_db


def update_plan(db: Session, updated_plan: schemas.Plan) -> models.Plan:
    stmt = (update(models.Plan)
            .where(models.Plan.id == updated_plan.id)
            .values(**updated_plan.model_dump())
            .returning(models.Plan))

    res = db.execute(stmt).scalar_one_or_none()
    db.commit()
    return res


def delete_plan(db: Session, plan_id: int) -> None:
    plan_db = db.query(models.Plan).get(plan_id)
    db.delete(plan_db)
    db.commit()

def get_plans_by_user_id(db:Session, user_id: int) -> list[Type[models.Plan]]:
    return db.query(models.Plan).filter(models.Plan.user_id == user_id).all()


def create_training_session(db: Session, training_session: schemas.TrainingSessionBase) -> models.TrainingSession:
    session_db = models.TrainingSession(**training_session.model_dump())
    db.add(session_db)
    db.commit()
    db.refresh(session_db)
    return session_db


def get_training_session_by_id(db: Session, session_id: int) -> models.TrainingSession:
    return db.query(models.TrainingSession).get(session_id)


def get_training_sessions_by_user_id(db: Session, user_id: int) -> list[Type[models.TrainingSession]]:
    return (db.query(models.TrainingSession)
            .join(models.Training).join(models.User)
            .where(models.User.id == user_id)
            .all())


def create_exercise_in_session(db: Session, ex_session_base: schemas.ExerciseInSessionBase) -> models.ExerciseInSession:
    ex_db = models.ExerciseInSession(**ex_session_base.model_dump())
    db.add(ex_db)
    db.commit()
    db.refresh(ex_db)
    return ex_db


def get_exercises_in_session(db: Session, session_id: int) -> list[Type[models.ExerciseInSession]]:
    return db.query(models.ExerciseInSession).filter(models.ExerciseInSession.training_session_id == session_id).all()
