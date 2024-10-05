import datetime

from pydantic import Field

from src.models.enums import TrainingType
from src.schemas.workout_exercise import WorkoutExerciseDetails, WorkoutExerciseCreate
from src.schemas.base_schema import BaseSchema


class WorkoutBase(BaseSchema):
    type: TrainingType | None = None
    notes: str | None = Field(max_length=1000)


class Workout(WorkoutBase):
    id: int
    workout_date: datetime.date

    class Config:
        from_attributes = True


class WorkoutDetails(Workout):
    workout_exercises: list[WorkoutExerciseDetails] = []


class WorkoutDetailsBase(WorkoutBase):
    workout_exercises: list[WorkoutExerciseCreate] = []


class WorkoutCreate(WorkoutDetailsBase):
    user_id: int


class WorkoutUpdate(BaseSchema):
    id: int
    notes: str | None = Field(max_length=1000)
    workout_date: datetime.date | None = None
    type: TrainingType | None = None

    class Config:
        from_attributes = True
