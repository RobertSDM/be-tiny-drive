from ..models import Account
from sqlalchemy.orm import Session, Query

def account_by_id(db: Session, id: str) -> Query[Account]:
    return db.query(Account).where(Account.id == id)
