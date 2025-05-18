from sqlalchemy.orm import Mapped, relationship, mapped_column
from datetime import datetime
from app.clients.sqlalchemy_client import Base


class Account(Base):
    __tablename__ = "tb_account"

    id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str]
    creation_date: Mapped[datetime]

    items: Mapped[list["Item"]] = relationship(cascade="delete", back_populates="owner")
