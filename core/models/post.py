from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, String, Text
from .mixins import UserRelationMixin


if TYPE_CHECKING:
    from .user import User


class Post(UserRelationMixin, Base):
    __tablename__ = "posts"
    __allow_unmapped__ = True

    _user_back_populates = "posts"

    title: Mapped[str] = mapped_column(String(100), unique=False)
    body: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.title!r}, user_id={self.user_id})"
