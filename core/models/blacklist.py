from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.types import Integer

from .base import Base

class Blacklist(Base):
    __tablename__ = "blacklist"
    
    user_id: Mapped[int] = mapped_column(Integer(), unique=True)