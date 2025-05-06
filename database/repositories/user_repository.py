from sqlalchemy import exists
from ..models import User
from sqlalchemy.orm import Session
from service.logging_config import logger


def user_exists_by_email(db: Session, email: str) -> bool:
    return db.query(exists().where(User.email == email)).scalar()


def user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()


def user_create(db: Session, user: User):
    db.add(user)
    db.commit()
    return user


def user_by_id(db: Session, id: int) -> User:
    return db.query(User).filter(User.id == id).first()
