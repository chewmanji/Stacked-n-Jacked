import datetime

from pydantic import BaseModel

from src.models.enums import Weekday, TrainingType


class TrainingBase(BaseModel):
    name: str
    weekday: Weekday | None = None
    type: TrainingType | None = None
    plan_id: int | None = None


class TrainingCreate(TrainingBase):
    user_id: int


class Training(TrainingBase):
    id: int

    class Config:
        from_attributes = True


class TrainingUpdate(BaseModel):
    id: int
    name: str | None = None
    weekday: Weekday | None = None
    type: TrainingType | None = None
    plan_id: int | None = None

    class Config:
        from_attributes = True


class TrainingSessionBase(BaseModel):
    session_date: datetime.date = datetime.date.today()
    training_id: int

    class Config:
        from_attributes = True


class TrainingSession(TrainingSessionBase):
    id: int

    class Config:
        from_attributes = True
