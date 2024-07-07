from .folder_model import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid


class File(Base):
    __tablename__ = "file"

    id = sa.Column(
        UUID(as_uuid=True),
        primary_key=True,
        name="file_id",
        default=uuid.uuid4,
        index=True,
    )
    name = sa.Column(sa.String)
    _type = sa.Column(sa.String, default="FILE")
    fullname = sa.Column(sa.String)
    extension = sa.Column(sa.String, nullable=False)
    byteSize = sa.Column(sa.Integer, nullable=False)
    prefix = sa.Column(sa.String, nullable=False)

    # User
    owner_id: Mapped["sa.UUID"] = mapped_column(
        sa.ForeignKey("user.user_id"), nullable=False
    )
    owner: Mapped["User"] = relationship(
        foreign_keys=[owner_id], back_populates="files", lazy="selectin"
    )

    # folder parent
    folder_id: Mapped["sa.UUID"] = mapped_column(
        sa.ForeignKey("folder.folder_id"), nullable=True
    )
    folder: Mapped["Folder"] = relationship(
        back_populates="files", foreign_keys=[folder_id], lazy="selectin"
    )

    fileData: Mapped["FileData"] = relationship(
        back_populates="file", uselist=False, lazy="selectin", cascade="all"
    )

    def __init__(self, name, extension, byteSize, prefix, byteData, folderId, ownerId):
        self.name = name
        self.fullname = f"{name}.{extension}"
        self.byteSize = byteSize
        self.extension = extension
        self.prefix = prefix
        self.folder_id = folderId
        self.owner_id = ownerId

        self.fileData = FileData(byteData=byteData)


class FileData(Base):
    __tablename__ = "fileData"

    id = sa.Column(
        UUID(as_uuid=True),
        primary_key=True,
        name="fileData_id",
        default=uuid.uuid4,
        index=True,
    )
    byteData: Mapped["sa.String"] = mapped_column(
        sa.String, nullable=False, deferred=True
    )
    file_id: Mapped["sa.UUID"] = mapped_column(
        sa.ForeignKey("file.file_id"), nullable=False
    )
    file: Mapped["File"] = relationship(back_populates="fileData", lazy="selectin")
