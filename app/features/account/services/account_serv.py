from sqlalchemy.orm import Session

from app.core.exceptions import AccountNotExists
from app.database.repositories.account_repo import account_by_id


def account_get_serv(db: Session, id: str):
    account = account_by_id(db, id).first()
    if not account:
        raise AccountNotExists()

    return account
