import datetime as dt
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String, Float, Integer
from sqlalchemy import ForeignKey

from .discipline import Discipline
from .student import Student
from .base import Base

class Queue(Base):
    __tablename__ = "queues"
    
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    discipline_id: Mapped[int] = mapped_column(ForeignKey("disciplines.id"))
    added_at: Mapped[float] = mapped_column(Float(), default=dt.datetime.now().timestamp())
    
    student: Mapped["Student"] = relationship(back_populates="queue")
    discipline: Mapped["Discipline"] = relationship(back_populates="queue")