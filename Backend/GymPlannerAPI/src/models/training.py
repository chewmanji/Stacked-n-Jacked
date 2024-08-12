import datetime

from sqlalchemy import Integer, String, Enum, ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.database import Base
from src.models.enums import Weekday, TrainingType
from src.models.plan import Plan
from src.models.user import User


class Training(Base):
    __tablename__ = "trainings"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    weekday: Mapped[Weekday] = mapped_column(Enum(Weekday), nullable=True)
    type: Mapped[TrainingType] = mapped_column(Enum(TrainingType), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id))
    plan_id: Mapped[int] = mapped_column(Integer, ForeignKey(Plan.id), nullable=True)

    user = relationship(User)
    plan = relationship(Plan)
    training_sessions = relationship("TrainingSession", back_populates="training")


class TrainingSession(Base):
    __tablename__ = "training_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_date: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today)
    training_id: Mapped[int] = mapped_column(Integer, ForeignKey(Training.id))

    training = relationship(Training)
    exercises_in_session = relationship("ExerciseInSession", back_populates="training_session")
