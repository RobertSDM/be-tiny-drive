from ..models.user_model import User
from sqlalchemy.orm import Session
from service.logging_config import logger


def find_user_by_email(db: Session, email: str) -> User:
    try:

        user = db.query(User).filter(User.email == email).first()
        return user

    except Exception as e:
        logger.error(e)
        return False


def insert_user(db: Session, user: User, salt: str):
    try:
        user = User(user.user_name, user.email, user.password, salt)
        db.add(user)
        db.commit()

        return True
    except Exception as e:
        logger.error(e)
        return False

def find_user_by_id(db: Session, id: str) -> User:
    try:
        user = db.query(User).filter(User.id == id).first()
        return user
    except Exception as e:
        logger.error(e)
        return False
