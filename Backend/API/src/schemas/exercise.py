import datetime
import re

from pydantic import HttpUrl, Field, field_validator
from src.schemas.base_schema import BaseSchema


class ExerciseBase(BaseSchema):
    id: int
    name: str


class ExerciseLatest(BaseSchema):
    id: int
    workout_date: datetime.date


class Exercise(ExerciseBase):
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
