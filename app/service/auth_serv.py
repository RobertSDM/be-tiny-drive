from sqlalchemy.orm import Session
from app.clients.supabase.auth_client import auth_client
from app.core.exceptions import AccountAlreadyExists, AccountRegistrationError
from app.database.models.account_model import Account
from app.database.repositories.account_repo import (
    account_by_email,
    account_save,
)
from app.utils.execute_query import execute_exists


def register_serv(db: Session, username: str, email: str, password: str) -> Account:
    exists = execute_exists(db, account_by_email(db, email))

    if exists:
        raise AccountAlreadyExists()

    resp = auth_client.register(email, password)
    if not resp.user:
        return AccountRegistrationError()

    account = Account(id=resp.user.id, username=username, email=resp.user.email, creation_date=resp.user.created_at)

    return account_save(db, account)
