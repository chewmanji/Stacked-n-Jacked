from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.models.training import Training, TrainingSession
from src.models.user import User


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    target_muscle: Mapped[str] = mapped_column(String(100))
    equipment: Mapped[str] = mapped_column(String(100), nullable=True)
    youtube_url: Mapped[str] = mapped_column(String, nullable=True)


class UserExercise(Base):
    __tablename__ = "user_exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    sets_number: Mapped[int] = mapped_column(Integer)
    reps_number: Mapped[int] = mapped_column(Integer)
    weight: Mapped[float] = mapped_column(Float, nullable=True)
    notes: Mapped[str] = mapped_column(String(255), nullable=True)
    exercise_id: Mapped[int] = mapped_column(Integer, ForeignKey(Exercise.id))
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id))
    training_id: Mapped[int] = mapped_column(Integer, ForeignKey(Training.id), nullable=True)

    exercise = relationship(Exercise)
    user = relationship(User)
    training = relationship(Training)


class ExerciseInSession(Base):
    __tablename__ = "exercises_in_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    sets_number: Mapped[int] = mapped_column(Integer)
    reps_number: Mapped[int] = mapped_column(Integer)
    weight: Mapped[float] = mapped_column(Float, nullable=True)
    user_exercise_id: Mapped[int] = mapped_column(Integer, ForeignKey(UserExercise.id))
    training_session_id: Mapped[int] = mapped_column(Integer, ForeignKey(TrainingSession.id))

    user_exercise = relationship(UserExercise)
    training_session = relationship(TrainingSession)
