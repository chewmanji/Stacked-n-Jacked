from pydantic import BaseModel, Field


class UserExerciseBase(BaseModel):
    sets_number: int = Field(ge=0, le=1000)
    reps_number: int = Field(ge=0, le=1000)
    weight: float | None = Field(default=None, ge=0, le=2000)
    notes: str | None = Field(default=None, max_length=255)
    exercise_id: int
    training_id: int | None = None


class UserExerciseCreate(UserExerciseBase):
    user_id: int


class UserExercise(UserExerciseBase):
    id: int

    class Config:
        from_attributes = True


class UserExerciseUpdate(BaseModel):
    id: int
    sets_number: int | None = Field(default=None, ge=0, le=1000)
    reps_number: int | None = Field(default=None, ge=0, le=1000)
    weight: float | None = Field(default=None, ge=0, le=2000)
    notes: str | None = Field(default=None, max_length=255)
    exercise_id: int | None = None
    training_id: int | None = None

    class Config:
        from_attributes = True


class ExerciseInSessionBase(BaseModel):
    sets_number: int = Field(ge=0, le=1000)
    reps_number: int = Field(ge=0, le=1000)
    weight: float | None = Field(default=None, ge=0, le=2000)
    user_exercise_id: int
    training_session_id: int


class ExerciseInSession(ExerciseInSessionBase):
    id: int

    class Config:
        from_attributes = True
