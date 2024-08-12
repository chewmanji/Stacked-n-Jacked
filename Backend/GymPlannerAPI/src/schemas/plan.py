import datetime

from pydantic import BaseModel, Field


class PlanBase(BaseModel):
    name: str = Field(max_length=50)
    start_date: datetime.date
    end_date: datetime.date | None = None
    goals: str | None = Field(default=None, max_length=50)


class PlanCreate(PlanBase):
    user_id: int


class Plan(PlanBase):
    id: int

    class Config:
        from_attributes = True


class PlanUpdate(BaseModel):
    id: int
    name: str | None = Field(default=None, max_length=50)
    start_date: datetime.date | None = None
    end_date: datetime.date | None = None
    goals: str | None = Field(default=None, max_length=50)

    class Config:
        from_attributes = True
