from sqlalchemy.orm import Session

from app.core.exceptions import AccountNotExists
from app.database.repositories.account_repo import account_by_id
from app.utils.query import exec_first


def account_get_serv(db: Session, id: str):
    account = exec_first(account_by_id(db, id))
    if not account:
        raise AccountNotExists()

    return account
