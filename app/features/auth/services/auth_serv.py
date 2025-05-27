from sqlalchemy.orm import Session
from app.core.select_dependency import get_auth_client_instance
from app.core.exceptions import AccountAlreadyExists, AccountRegistrationError
from app.database.models.account_model import Account
from app.database.repositories.account_repo import (
    account_by_email,
    account_save,
)
from app.utils.query import exec_exists


def register_serv(db: Session, username: str, email: str, password: str) -> Account:
    exists = exec_exists(db, account_by_email(db, email))

    if exists:
        raise AccountAlreadyExists()

    auth_client = get_auth_client_instance()
    resp = auth_client.registerPassword(email, password)
    if not resp:
        return AccountRegistrationError()

    account = Account(
        id=resp.id,
        username=username,
        email=resp.email,
        creation_date=resp.creation_date,
    )

    return account_save(db, account)
