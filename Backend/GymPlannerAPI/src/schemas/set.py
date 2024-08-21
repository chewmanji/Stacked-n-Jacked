from pydantic import BaseModel, Field


class SetBase(BaseModel):
    reps_count: int = Field(ge=0, le=1000)
    weight: float | None = Field(default=None, ge=0, le=2000)
    set_number: int = Field(ge=0, le=1000)
    notes: str | None = Field(default=None, max_length=150)
    workout_exercise_id: int


class SetCreate(SetBase):
    user_id: int


class Set(SetBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
