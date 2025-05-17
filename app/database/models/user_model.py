from typing import Optional
from uuid import uuid4
from sqlalchemy import func
from sqlalchemy.orm import Mapped, relationship, mapped_column
from datetime import datetime
from app.clients.sqlalchemy_client import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    salt: Mapped[str]
    creationDate: Mapped[float] = mapped_column(
        default=datetime.now().timestamp, server_default=func.current_timestamp()
    )

    items: Mapped[list["Item"]] = relationship(cascade="all", back_populates="owner")
