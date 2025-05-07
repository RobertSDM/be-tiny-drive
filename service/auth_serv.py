import bcrypt
from sqlalchemy.orm import Session
from core.exeptions import InvalidPassword, UserAlreadyExists, UserDoesNotExists
from database.models import User
from auth.jwt import authenticate_token, create_token
from database.repositories.user_repo import (
    user_by_email,
    user_by_id,
    user_create,
)
from database.repositories.utils import execute_exists, execute_first
from core.schemas import LoginReturn, UserModel
from service.item_serv import create_root_item
from auth.password_hashing import hash_password, check_password_hash


def login_serv(db: Session, email: str, password: str) -> LoginReturn:
    user = execute_first(db, user_by_email(db, email))

    if not user:
        raise UserDoesNotExists()

    is_password_valid = check_password_hash(user.password, password)

    if not is_password_valid:
        raise InvalidPassword()

    token = create_token(user.id)

    return LoginReturn(
        token=token,
        user=UserModel.model_validate(user),
    )


def register_serv(db: Session, username: str, email: str, password: str) -> User:
    user_exists = execute_exists(db, user_by_email(db, email))

    if user_exists:
        raise UserAlreadyExists()

    salt = bcrypt.gensalt().decode()

    user = User(
        username=username,
        email=email,
        password=hash_password(password, salt),
        salt=salt,
    )

    user = user_create(db, user)
    create_root_item(db, user.id)

    return user


def __cut_header_token(header_token: str) -> str:
    return header_token.replace("Bearer ", "")


def validate_token_serv(db: Session, header_token: str):
    token = __cut_header_token(header_token)

    userId = authenticate_token(token)

    if not isinstance(userId, str):
        return userId

    userExist = user_by_id(db, userId)

    if not userExist:
        return {"status": 200, "content": {"msg": "The token is invalid", "data": None}}

    return True
