from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import func
from pydantic import BaseModel, ConfigDict
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .order_product_association import order_product_association_table


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

    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    orders: Mapped[list["Order"]] = relationship(
        secondary="order_product_association",
        back_populates="products",
    )
    orders_details: Mapped["OrderProductAssociation"] = relationship(back_populates="product")
