import datetime

from sqlalchemy import Integer, String, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.models.enums import Gender


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    hashed_password: Mapped[str] = mapped_column(String)
    birth_date: Mapped[datetime.date] = mapped_column(Date)
    gender: Mapped[Gender] = mapped_column(Enum(Gender), default=Gender.Unknown)
    #created at updated at???

    workout_exercises = relationship("WorkoutExercise", back_populates="user")
    workouts = relationship("Workout", back_populates="user")
