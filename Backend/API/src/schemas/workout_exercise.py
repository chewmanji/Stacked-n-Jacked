from pydantic import BaseModel, Field
from src.schemas.set import Set
from src.schemas.exercise import ExerciseBase


class WorkoutExerciseBase(BaseModel):
    notes: str | None = Field(default=None, max_length=300)
    exercise_id: int
    workout_id: int


# class WorkoutExerciseCreate(WorkoutExerciseBase):
#     workout_id: int


class WorkoutExercise(WorkoutExerciseBase):
    id: int

    class Config:
        from_attributes = True


class WorkoutExerciseDetails(WorkoutExercise):
    sets: list[Set]
    exercise: ExerciseBase


class WorkoutExerciseUpdate(BaseModel):
    id: int
    notes: str | None = Field(default=None, max_length=255)
    exercise_id: int | None = None

    class Config:
        from_attributes = True
