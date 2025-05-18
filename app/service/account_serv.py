from sqlalchemy.orm import Session

from app.core.exceptions import AccountDoesNotExists
from app.database.repositories.account_repo import account_by_id
from app.utils.execute_query import execute_first


def account_get_serv(db: Session, id: str):
    account = execute_first(account_by_id(db, id))
    if not account:
        raise AccountDoesNotExists()

    return account
