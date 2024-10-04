from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.models.workout import Workout
from src.models.exercise import Exercise


class WorkoutExercise(Base):
    __tablename__ = "workout_exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    notes: Mapped[str] = mapped_column(String(300), nullable=True)
    exercise_id: Mapped[int] = mapped_column(Integer, ForeignKey(Exercise.id), nullable=False)
    workout_id: Mapped[int] = mapped_column(Integer, ForeignKey(Workout.id), nullable=False)

    exercise = relationship(Exercise)
    workout = relationship(Workout)
    sets = relationship('Set', back_populates='workout_exercise')
