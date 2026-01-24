from sqlalchemy.orm import Session

from app.core.exceptions import AccountNotExists
from app.database.repositories.account_repo import account_by_id


class AccountService:
    def account_by_id(db: Session, id: str):
        account = account_by_id(db, id).first()
        if not account:
            raise AccountNotExists()

        return account
