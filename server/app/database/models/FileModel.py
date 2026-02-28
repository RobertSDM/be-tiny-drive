from typing import Optional
from uuid import uuid4

from sqlalchemy import ForeignKey
from server.app.lib.sqlalchemy import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime, timezone


class FileModel(Base):
    __tablename__ = "tb_file"

    filename: Mapped[str]
    extension: Mapped[str]
    size: Mapped[int]
    size_prefix: Mapped[str]
    content_type: Mapped[str]

    parentid: Mapped[Optional[str]] = mapped_column(
        ForeignKey("tb_file.id"), index=True
    )

    children: Mapped[list["FileModel"]] = relationship(cascade="all", init=False)

    ownerid: Mapped[Optional[str]] = mapped_column(ForeignKey("tb_user_account.id"))

    # Declaring at last because of python dataclass
    id: Mapped[str] = mapped_column(
        primary_key=True, default_factory=lambda: str(uuid4())
    )
    is_dir: Mapped[bool] = mapped_column(name="is_directory", default=False)

    updated_at: Mapped[datetime] = mapped_column(
        default_factory=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        # server_default=func.current_timestamp(),
    )

    created_at: Mapped[datetime] = mapped_column(
        default_factory=lambda: datetime.now(timezone.utc),
        # server_default=func.current_timestamp(),
    )
