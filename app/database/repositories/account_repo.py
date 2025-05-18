from ..models import Account
from sqlalchemy.orm import Session, Query


def account_by_id(db: Session, id: str) -> Query[Account]:
    return db.query(Account).where(Account.id == id)


def account_by_email(db: Session, email: str) -> Query[Account]:
    return db.query(Account).where(Account.email == email)


def account_save(db: Session, account: Account) -> Account:
    db.add(account)
    db.commit()
    return account
