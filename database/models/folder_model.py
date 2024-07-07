from ..init_database import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid


class Folder(Base):
    __tablename__ = "folder"

    id = sa.Column(
        UUID(as_uuid=True),
        primary_key=True,
        name="folder_id",
        default=uuid.uuid4,
        index=True,
    )
    name = sa.Column(sa.String, nullable=False)
    _type = sa.Column(sa.String, default="FOLDER")
    tray = sa.Column(sa.String, nullable=False, default="")

    # Child folders
    folders: Mapped[list["Folder"]] = relationship(
        back_populates="folder", cascade="all"
    )

    # User
    owner_id: Mapped["sa.UUID"] = mapped_column(
        sa.ForeignKey("user.user_id"), nullable=False
    )
    owner: Mapped["User"] = relationship(
        foreign_keys=[owner_id], back_populates="folders", lazy="selectin"
    )

    # Parent folders
    folderC_id: Mapped["sa.UUID"] = mapped_column(
        sa.ForeignKey("folder.folder_id"), nullable=True
    )
    folder: Mapped["Folder"] = relationship(
        back_populates="folders",
        foreign_keys=[folderC_id],
        remote_side=[id],
        lazy="selectin",
    )

    # files relation
    files: Mapped[list["File"]] = relationship(back_populates="folder", cascade="all")

    def __init__(self, name: str, folder_id: str, owner_id: str):
        self.name = name
        self.folderC_id = folder_id
        self.owner_id = owner_id

    def set_tray(self, parentTray):
        if self.folderC_id:
            self.tray = f"{parentTray}/{self.name};{str(self.id)}"
        else:
            self.tray = f"{self.name};{str(self.id)}"
