from ..db_engine import Base
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, relationship, mapped_column


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    salt: Mapped[str]

    items: Mapped[list["Item"]] = relationship(cascade="all", back_populates="owner")
