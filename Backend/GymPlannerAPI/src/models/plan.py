# import datetime
#
# from sqlalchemy import Integer, String, Date, ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from src.core.database import Base
# from src.models.user import User
#
#
# class Plan(Base):
#     __tablename__ = "plans"
#
#     id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String(50))
#     start_date: Mapped[datetime.date] = mapped_column(Date)
#     end_date: Mapped[datetime.date] = mapped_column(Date, nullable=True)
#     goals: Mapped[str] = mapped_column(String(50), nullable=True)
#     user_id: Mapped[int] = mapped_column(Integer, ForeignKey(User.id))
#
#     user = relationship(User)
