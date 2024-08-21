from pydantic import BaseModel, Field


class WorkoutExerciseBase(BaseModel):
    notes: str | None = Field(default=None, max_length=300)
    exercise_id: int
    workout_id: int


class WorkoutExerciseCreate(WorkoutExerciseBase):
    user_id: int
    workout_id: int


class WorkoutExercise(WorkoutExerciseBase):
    id: int


    class Config:
        from_attributes = True


class WorkoutExerciseUpdate(BaseModel):
    id: int
    notes: str | None = Field(default=None, max_length=255)
    exercise_id: int | None = None

    class Config:
        from_attributes = True
