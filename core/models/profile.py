from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship
from .mixins import UserRelationMixin


if TYPE_CHECKING:
    from .user import User


class Profile(Base):
    _user_id_unique = True
    _user_back_populates = "profile"

    first_name: Mapped[str] = mapped_column(String(40), unique=False)
    last_name: Mapped[str] | None = mapped_column(String(40), unique=False)
    bio: Mapped[str | None]
