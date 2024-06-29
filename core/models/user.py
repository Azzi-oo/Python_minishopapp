from pydantic import BaseModel, ConfigDict
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class User(Base):
    __tablename__ = "users"
    __allow_unmapped__ = True

    name: Mapped[str] = mapped_column(unique=True)
    price: Mapped[int]
    description: Mapped[str]
