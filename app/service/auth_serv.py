import bcrypt
from sqlalchemy.orm import Session
from app.core.exceptions import UserAlreadyExists
from app.database.models import User
from app.database.repositories.account_repo import (
    user_by_email,
    user_by_id,
)
from app.utils.execute_query import execute_exists, execute_first


def register_serv(db: Session, username: str, email: str, password: str) -> None:
    exists = execute_exists(db, user_by_email(db, email))

    if exists:
        raise UserAlreadyExists()

    return
