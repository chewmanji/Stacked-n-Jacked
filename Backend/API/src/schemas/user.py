import datetime

from pydantic import BaseModel, EmailStr

from src.models.enums import Gender


class UserBase(BaseModel):
    email: EmailStr
    birth_date: datetime.date
    gender: Gender | None = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int


    class Config:
        from_attributes = True
