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

    user_exercises = relationship("UserExercise", back_populates="user")
    plans = relationship("Plan", back_populates="user")
    trainings = relationship("Training", back_populates="user")
