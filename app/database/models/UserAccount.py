from uuid import uuid4
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from app.lib.sqlalchemy import Base


class UserAccount(Base):
    __tablename__ = "tb_user_account"

    username: Mapped[str]
    email: Mapped[str]
    created_at: Mapped[datetime]

    # Declaring at last because of python dataclass
    id: Mapped[str] = mapped_column(primary_key=True)
