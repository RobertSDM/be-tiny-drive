from sqlalchemy import exists
from ..models import User
from sqlalchemy.orm import Session, Query


def user_by_email(db: Session, email: str) -> Query[User]:
    return db.query(User).where(User.email == email)


def user_create(db: Session, user: User):
    db.add(user)
    db.commit()
    return user


def user_by_id(db: Session, id: int) -> Query[User]:
    return db.query(User).filter(User.id == id)
