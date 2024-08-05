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


def get_user(db: Session, user_id: int) -> models.User | None:
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


def get_user_exercises(db: Session, user_id: int) -> list[Type[models.UserExercise]]:
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