import datetime

from sqlalchemy import Integer, String, ForeignKey, Enum, Date, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.models.enums import TrainingType


class Workout(Base):
    __tablename__ = 'workouts'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    workout_date: Mapped[datetime.date] = mapped_column(Date, server_default=func.now())
    type: Mapped[TrainingType] = mapped_column(Enum(TrainingType), nullable=True)
    notes: Mapped[str] = mapped_column(String(1000), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)

    workout_exercises = relationship('WorkoutExercise', back_populates="workout")
    user = relationship('User')
