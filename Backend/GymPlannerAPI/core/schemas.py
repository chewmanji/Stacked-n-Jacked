import datetime
import re
from pydantic import BaseModel, Field, HttpUrl, field_validator, EmailStr
from sqlalchemy.orm import Session
from core.models import Gender, Weekday, TrainingType
import core.crud as crud


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None


class Exercise(BaseModel):
    id: int
    name: str
    target_muscle: str
    equipment: str | None = None
    youtube_url: HttpUrl | None = Field(default=None, description="URL to Youtube video tutorial for an exercise",
                                        max_length=100)

    @field_validator('youtube_url')
    def validate_youtube_url(cls, v):
        if v is None:
            return v

        youtube_pattern = r"^https?://(?:(?:www\.)?youtube\.com/watch\?v=|youtu\.be/)[\w-]{11}$"
        if not re.match(youtube_pattern, str(v)):
            raise ValueError("Invalid YouTube URL")
        return v

    class Config:
        from_attributes = True


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


class TrainingSessionBase(BaseModel):
    session_date: datetime.date = datetime.date.today()
    training_id: int

    class Config:
        from_attributes = True


class TrainingSession(TrainingSessionBase):
    id: int

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


class UserBase(BaseModel):
    email: EmailStr
    birth_date: datetime.date
    gender: Gender | None = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    # user_exercises: list[UserExercise] = []
    # trainings: list[Training] = []
    # plans: list[Plan] = []

    class Config:
        from_attributes = True

    # def has_access_to_training(self,  training_id: int, db: Session) -> bool:
    #     trainings = crud.get_trainings_by_user_id(db, self.id)
    #     return any(training.id == training_id for training in trainings)
    #
    # def has_access_to_user_exercise(self,  user_exercise_id: int, db: Session) -> bool:
    #     user_exercises = crud.get_user_exercises_by_user_id(db, self.id)
    #     return any(user_exercise.id == user_exercise_id for user_exercise in user_exercises)
    #
    # def has_access_to_plan(self,  plan_id: int, db: Session) -> bool:
    #     plans = crud.get_plans_by_user_id(db, self.id)
    #     return any(plan.id == plan_id for plan in plans)
