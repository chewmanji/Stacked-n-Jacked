from sqlalchemy import Integer, String, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.models.workout_exercise import WorkoutExercise


class Set(Base):
    __tablename__ = 'sets'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    reps_count: Mapped[int] = mapped_column(Integer)
    weight: Mapped[float] = mapped_column(Float)
    set_number: Mapped[int] = mapped_column(Integer)
    notes: Mapped[str] = mapped_column(String(150), nullable=True)
    workout_exercise_id: Mapped[int] = mapped_column(Integer, ForeignKey('workout_exercises.id'), nullable=False)

    workout_exercise = relationship(WorkoutExercise)