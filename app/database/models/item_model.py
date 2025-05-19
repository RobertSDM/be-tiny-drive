from typing import Optional
from uuid import uuid4
from sqlalchemy import ForeignKey, func
from app.enums.enums import ItemType
from app.clients.sqlalchemy_client import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime


class Item(Base):
    __tablename__ = "tb_item"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str]
    extension: Mapped[str]
    path: Mapped[str]
    size: Mapped[int]
    size_prefix: Mapped[str]
    bucketid: Mapped[Optional[str]]
    type: Mapped[ItemType]
    update_date: Mapped[float] = mapped_column(
        default=datetime.now().timestamp,
        onupdate=datetime.now().timestamp,
        server_default=func.current_timestamp(),
    )
    creation_date: Mapped[float] = mapped_column(
        default=datetime.now().timestamp,
        server_default=func.current_timestamp(),
    )

    # parent item
    parentid: Mapped[Optional[str]] = mapped_column(ForeignKey("tb_item.id"))
    parent: Mapped["Item"] = relationship(back_populates="items", remote_side=[id])

    # children of this item
    items: Mapped[list["Item"]] = relationship(back_populates="parent", cascade="all")

    # owner
    ownerid: Mapped[Optional[str]] = mapped_column(ForeignKey("tb_account.id"))
    owner: Mapped["Account"] = relationship(back_populates="items")
