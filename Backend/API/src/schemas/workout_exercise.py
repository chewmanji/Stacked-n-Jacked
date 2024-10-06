import datetime
from pydantic import Field
from src.schemas.set import Set, SetCreate
from src.schemas.exercise import ExerciseBase
from src.schemas.base_schema import BaseSchema


class WorkoutExerciseBase(BaseSchema):
    notes: str | None = Field(default=None, max_length=300)
    exercise_id: int
    workout_id: int


class WorkoutExercise(WorkoutExerciseBase):
    id: int

    class Config:
        from_attributes = True


class WorkoutExerciseDetails(WorkoutExercise):
    sets: list[Set]
    exercise: ExerciseBase


class WorkoutExerciseDetailsChart(BaseSchema):
    id: int
    workout_date: datetime.date | None = None
    sets: list[Set]


class WorkoutExerciseCreate(BaseSchema):
    sets: list[SetCreate]
    exercise_id: int


class WorkoutExerciseUpdate(BaseSchema):
    id: int
    notes: str | None = Field(default=None, max_length=255)
    exercise_id: int | None = None

    class Config:
        from_attributes = True
