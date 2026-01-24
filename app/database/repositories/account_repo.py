from app.database.models import UserAccount
from sqlalchemy.orm import Session, Query


def account_by_id(db: Session, id: str) -> Query[UserAccount]:
    return db.query(UserAccount).where(UserAccount.id == id)


def account_by_email(db: Session, email: str) -> Query[UserAccount]:
    return db.query(UserAccount).where(UserAccount.email == email)


def account_save(db: Session, account: UserAccount) -> None:
    db.add(account)
    db.flush()
