from pydantic import  Field
from src.schemas.base_schema import BaseSchema


class SetBase(BaseSchema):
    reps_count: int = Field(ge=0, le=1000)
    weight: float | None = Field(default=None, ge=0, le=2000)
    set_number: int = Field(ge=0, le=1000)
    notes: str | None = Field(default=None, max_length=150)
    workout_exercise_id: int


class Set(SetBase):
    id: int
    workout_exercise_id: int

    class Config:
        from_attributes = True


class SetCreate(BaseSchema):
    reps_count: int = Field(ge=0, le=1000)
    set_number: int = Field(ge=0, le=1000)
    weight: float | None = Field(default=None, ge=0, le=2000)
