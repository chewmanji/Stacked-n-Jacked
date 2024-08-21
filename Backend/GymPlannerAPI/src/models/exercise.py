from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    target_muscle: Mapped[str] = mapped_column(String(100))
    equipment: Mapped[str] = mapped_column(String(100), nullable=True)
    youtube_url: Mapped[str] = mapped_column(String, nullable=True)

# class ExerciseInSession(Base):
#     __tablename__ = "exercises_in_sessions"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True)
#     sets_number: Mapped[int] = mapped_column(Integer)
#     reps_number: Mapped[int] = mapped_column(Integer)
#     weight: Mapped[float] = mapped_column(Float, nullable=True)
#     user_exercise_id: Mapped[int] = mapped_column(Integer, ForeignKey(UserExercise.id))
#     training_session_id: Mapped[int] = mapped_column(Integer, ForeignKey(TrainingSession.id))
#
#     user_exercise = relationship(UserExercise)
#     training_session = relationship(TrainingSession)
