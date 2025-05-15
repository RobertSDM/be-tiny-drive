from typing import Optional
from sqlalchemy import ForeignKey
from .enums.content_type import ItemType
from ..db_engine import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime


class Item(Base):
    __tablename__ = "tb_item"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    extension: Mapped[str]
    path: Mapped[str] = mapped_column()
    size: Mapped[int]
    size_prefix: Mapped[str]
    type: Mapped[ItemType]
    data: Mapped[bytes]
    update_date: Mapped[float] = mapped_column(
        default=datetime.now().timestamp, onupdate=datetime.now().timestamp
    )
    creation_date: Mapped[float] = mapped_column(
        default=datetime.now().timestamp
    )

    # parent item
    parentid: Mapped[Optional[int]] = mapped_column(ForeignKey("tb_item.id"))
    parent: Mapped["Item"] = relationship(back_populates="items", remote_side=[id])

    # children of this item
    items: Mapped[list["Item"]] = relationship(back_populates="parent", cascade="all")

    # owner
    ownerid: Mapped[Optional[int]] = mapped_column(ForeignKey("user.id"))
    owner: Mapped["User"] = relationship(back_populates="items")
