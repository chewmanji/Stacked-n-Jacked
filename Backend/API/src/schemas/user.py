import datetime

from pydantic import EmailStr
from src.schemas.base_schema import BaseSchema

from src.models.enums import Gender


class UserBase(BaseSchema):
    email: EmailStr
    birth_date: datetime.date
    gender: Gender | None = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserUpdate(BaseSchema):
    id: int | None = None
    email: EmailStr | None = None
    password: str | None = None
    birth_date: datetime.date | None = None
    gender: Gender | None = None
