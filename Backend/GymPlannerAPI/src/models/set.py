from sqlalchemy import Integer, String, ForeignKey, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.models.exercise import WorkoutExercise


class Set(Base):
    __tablename__ = 'sets'

    id: Mapped[int] = mapped_column('id', Integer, primary_key=True, autoincrement=True),
    reps_count: Mapped[int] = mapped_column('reps_count', Integer),
    weight: Mapped[float] = mapped_column('weight', DECIMAL(precision=3, scale=6)),
    set_number: Mapped[int] = mapped_column('set_number', Integer),
    notes: Mapped[str] = mapped_column('notes', String(150), nullable=True),
    workout_exercise_id: Mapped[int] = mapped_column('workout_exercise_id', Integer, ForeignKey('workout_exercises.id'), nullable=False),
    user_id: Mapped[int] = mapped_column('user_id', Integer, ForeignKey('users.id'), nullable=False)

    workout_exercise = relationship(WorkoutExercise)