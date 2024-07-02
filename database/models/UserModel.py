from .FileModel import Base
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.dialects.postgresql import UUID
import uuid


class User(Base):
    __tablename__ = "user"

    id = sa.Column(
        UUID(as_uuid=True),
        primary_key=True,
        name="user_id",
        default=uuid.uuid4,
        index=True,
    )
    user_name = sa.Column(sa.String, nullable=False)
    email = sa.Column(sa.String, nullable=False)
    password = sa.Column(sa.String, nullable=False)
    salt = sa.Column(sa.String, nullable=False)

    # Folders
    folders: Mapped[list["Folder"]] = relationship(
        cascade="all", back_populates="owner"
    )

    # Files
    files: Mapped[list["File"]] = relationship(cascade="all", back_populates="owner")

    def __init__(self, user_name: str, email: str, _pass: str, salt: str):
        self.user_name = user_name
        self.email = email
        self.password = _pass
        self.salt = salt
