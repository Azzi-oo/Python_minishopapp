from typing import TYPE_CHECKING
from pydantic import BaseModel, ConfigDict
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from sqlalchemy.orm import relationship


if TYPE_CHECKING:
    from .post import Post
    from .profile import Profile


class User(Base):
    __tablename__ = "users"
    __allow_unmapped__ = True

    username: Mapped[str] = mapped_column(unique=True)

    posts: Mapped["Post"] = relationship(back_populates="posts")
    profile: Mapped["Profile"] = relationship(back_populates="users")
