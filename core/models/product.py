from pydantic import BaseModel, ConfigDict
from .base import Base
from sqlalchemy.orm import Mapped


class ProductBase(Base):
    __tablename__ = "products"
    __allow_unmapped__ = True

    name: Mapped[str]
    price: Mapped[int]
    description: Mapped[str]


class ProductCreate(BaseModel):
    pass


class Product(ProductBase):
    model_config = ConfigDict(from_attribute=True)

    id: int
