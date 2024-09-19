from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.core.database import Base


class Exercise(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    target_muscle: Mapped[str] = mapped_column(String(100))
    equipment: Mapped[str] = mapped_column(String(100), nullable=True)
    youtube_url: Mapped[str] = mapped_column(String, nullable=True)

