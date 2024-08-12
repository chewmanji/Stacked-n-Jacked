import re

from pydantic import BaseModel, HttpUrl, Field, field_validator


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
