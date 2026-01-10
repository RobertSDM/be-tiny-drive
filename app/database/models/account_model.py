from uuid import uuid4
from sqlalchemy.orm import Mapped, relationship, mapped_column
from datetime import datetime
from app.lib.sqlalchemy import Base


class UserAccount(Base):
    __tablename__ = "tb_user_account"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    username: Mapped[str]
    email: Mapped[str]
    created_at: Mapped[datetime]

    files: Mapped[list["File"]] = relationship(cascade="delete", back_populates="owner")
