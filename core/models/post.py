from pydantic import BaseModel, ConfigDict
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, String, Text


class Post(Base):
    __tablename__ = "posts"
    __allow_unmapped__ = True

    title: Mapped[str] = mapped_column(String(32), unique=False)
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
    )
