from typing import List
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import String

from .base import Base

class Discipline(Base):
    __tablename__ = "disciplines"
    
    name: Mapped[str] = mapped_column(String(16), unique=True, nullable=False)
    
    queue: Mapped[List["Queue"]] = relationship(back_populates="discipline", cascade="all, delete-orphan")