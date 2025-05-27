from typing import Optional
from uuid import uuid4
from sqlalchemy import ForeignKey, func
from app.enums.enums import ItemType
from app.database.client.sqlalchemy_client import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timezone


class Item(Base):
    __tablename__ = "tb_item"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str]
    extension: Mapped[str]
    size: Mapped[int]
    size_prefix: Mapped[str]
    type: Mapped[ItemType]
    content_type: Mapped[str]
    update_date: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        server_default=func.current_timestamp(),
    )
    creation_date: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
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
