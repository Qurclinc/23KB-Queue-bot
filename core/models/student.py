from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Integer

from .base import Base

class Student(Base):
    __tablename__ = "students"
    
    user_id: Mapped[int] = mapped_column(Integer, unique=True)
    usertag: Mapped[str] = mapped_column(String(64), unique=True, nullable=True)
    username: Mapped[str] = mapped_column(String(32), nullable=False)
    
    queue: Mapped[List["Queue"]] = relationship(back_populates="student", cascade="all, delete-orphan")