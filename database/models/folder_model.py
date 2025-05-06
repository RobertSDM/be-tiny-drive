from ..db_engine import Base
from sqlalchemy.orm import relationship, Mapped, mapped_column
import sqlalchemy as sa


class Folder(Base):
    __tablename__ = "folder"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True,
    )
    name: Mapped[str]
    _type: Mapped[str] = mapped_column(default="FOLDER")
    tray: Mapped[str] = mapped_column(default="")

    # Child folders
    folders: Mapped[list["Folder"]] = relationship(
        back_populates="folder", cascade="all"
    )

    # User
    owner_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"), nullable=False)
    owner: Mapped["User"] = relationship(
        foreign_keys=[owner_id], back_populates="folders", lazy="selectin"
    )

    # Parent folders
    folderC_id: Mapped[int] = mapped_column(
        sa.ForeignKey("folder.id"), nullable=True
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

    def update_tray(self, parentTray, newName, updatedTray={}):
        if self.folderC_id:
            self.tray = f"{parentTray}/{newName};{str(self.id)}"
        else:
            self.tray = f"{newName};{str(self.id)}"

        updatedTray[str(self.id)] = self.tray

        for i in self.folders:
            i.update_tray(self.tray, i.name, updatedTray)

        return updatedTray
