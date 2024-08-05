import datetime

from sqlalchemy import ForeignKey, Integer, String, Enum, Date, Float
from sqlalchemy.orm import relationship, Mapped, mapped_column
import enum
from core.database import Base


class Gender(enum.Enum):
    Male = 0
    Female = 1
    Unknown = 2


class Weekday(enum.Enum):
    Monday = 1
    Tuesday = 2
    Wednesday = 3
    Thursday = 4
    Friday = 5
    Saturday = 6
    Sunday = 7


class TrainingType(enum.Enum):
    FBW = "FBW"
    Push = "Push"
    Pull = "Pull"
    Upper = "Upper"
    Lower = "Lower"
    Custom = "Custom"


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




class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    target_muscle: Mapped[str] = mapped_column(String(100))
    equipment: Mapped[str] = mapped_column(String(100), nullable=True)
    youtube_url: Mapped[str] = mapped_column(String, nullable=True)


class Plan(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    start_date: Mapped[datetime.date] = mapped_column(Date)
    end_date: Mapped[datetime.date] = mapped_column(Date, nullable=True)
    goals: Mapped[str] = mapped_column(String(50), nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id))

    user = relationship(User)


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


class TrainingSession(Base):
    __tablename__ = "training_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_date: Mapped[datetime.date] = mapped_column(Date, default=datetime.date.today)
    training_id: Mapped[int] = mapped_column(Integer, ForeignKey(Training.id))

    training = relationship(Training)
    exercises_in_session = relationship("ExerciseInSession", back_populates="training_session")


class ExerciseInSession(UserExercise):
    __tablename__ = "exercises_in_sessions"

    user_exercise_id: Mapped[int] = mapped_column(Integer, ForeignKey(UserExercise.id), primary_key=True)
    training_session_id: Mapped[int] = mapped_column(Integer, ForeignKey(TrainingSession.id), primary_key=True)

    user_exercise = relationship(UserExercise)
    training_session = relationship(TrainingSession)