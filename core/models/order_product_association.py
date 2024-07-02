from typing import TYPE_CHECKING
from sqlalchemy import Table, Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


if TYPE_CHECKING:
    from .order import Order
    from .product import Product


class OrderProductAssociation(Base):
    __tablename__ = "order_product_association"
    __table_args__ = [
        UniqueConstraint("order_id", "product_id", name="idx_unique_order_product",)
    ]

    id: Mapped[int] = mapped_column(primary_key=True)
    order_od: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    count: Mapped[int] = mapped_column(default=0)
    unit_price: Mapped[int] = mapped_column(default=1, server_default="1", nullable=False)
    child: Mapped["Order"] = relationship(back_populates="parent_association")

    parent: Mapped["Product"] = relationship(back_populates="child_association")
