from typing import Optional
from uuid import uuid4

from sqlalchemy import ForeignKey
from app.core.schemas import FileType
from app.lib.sqlalchemy import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timezone


class File(Base):
    __tablename__ = "tb_file"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    filename: Mapped[str]
    extension: Mapped[str]
    size: Mapped[int]
    size_prefix: Mapped[str]
    type: Mapped[FileType]
    content_type: Mapped[str]
    to_delete: Mapped[bool] = mapped_column(
        default=False
    )  # date when the file will be deleted

    updated_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        # server_default=func.current_timestamp(),
    )

    created_at: Mapped[datetime] = mapped_column(
        default=lambda: datetime.now(timezone.utc),
        # server_default=func.current_timestamp(),
    )

    parentid: Mapped[Optional[str]] = mapped_column(ForeignKey("tb_file.id"))
    parent: Mapped["File"] = relationship(back_populates="children", remote_side=[id])

    children: Mapped[list["File"]] = relationship(
        back_populates="parent", cascade="all"
    )

    ownerid: Mapped[Optional[str]] = mapped_column(ForeignKey("tb_user_account.id"))
    owner: Mapped["UserAccount"] = relationship(back_populates="files")
