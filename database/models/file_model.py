from enum import Enum
from typing import Optional
from sqlalchemy import ForeignKey, String
from ..db_engine import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid


class FileType(Enum):
    FILE = "FILE"
    FOLDER = "FOLDER"


class File(Base):
    __tablename__ = "file"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(30))
    type: Mapped[FileType]
    filename: Mapped[str]
    extension: Mapped[str]
    byteSize: Mapped[int]
    prefix: Mapped[str]

    # User
    owner_id: Mapped[str] = mapped_column(ForeignKey("user.id"))
    owner: Mapped["User"] = relationship(back_populates="files", lazy="selectin")

    # folder parent
    folder_id: Mapped[Optional[str]] = mapped_column(ForeignKey("folder.id"))
    folder: Mapped["Folder"] = relationship(back_populates="files", lazy="selectin")

    # FileData
    fileData: Mapped["FileData"] = relationship(
        back_populates="file", lazy="selectin", cascade="all"
    )


class FileData(Base):
    __tablename__ = "fileData"

    id: Mapped[str] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
        index=True,
    )
    byteData: Mapped[bytes] = mapped_column(deferred=True)

    file_id: Mapped[str] = mapped_column(ForeignKey("file.file_id"))
    file: Mapped["File"] = relationship(back_populates="fileData", lazy="selectin")
