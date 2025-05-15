import bcrypt
from sqlalchemy.orm import Session
from app.core.exeptions import InvalidPassword, UserAlreadyExists, UserDoesNotExists
from app.database.models import User
from app.auth.jwt import authenticate_token, create_token
from app.database.repositories.user_repo import (
    user_by_email,
    user_by_id,
    user_save,
)
from app.utils.execute_query import execute_exists, execute_first
from app.core.schemas import LoginReturn, UserModel
from app.auth.password_hashing import hash_password, check_password_hash


def login_serv(db: Session, email: str, password: str) -> LoginReturn:
    user = execute_first(user_by_email(db, email))

    if not user:
        raise UserDoesNotExists()

    is_valid = check_password_hash(user.password, password)

    if not is_valid:
        raise InvalidPassword()

    token = create_token(user.id)

    return LoginReturn(
        token=token,
        user=UserModel.model_validate(user),
    )


def register_serv(db: Session, username: str, email: str, password: str) -> User:
    exists = execute_exists(db, user_by_email(db, email))

    if exists:
        raise UserAlreadyExists()

    salt = bcrypt.gensalt().decode()

    user = User(
        username=username,
        email=email,
        password=hash_password(password, salt),
        salt=salt,
    )

    user = user_save(db, user)

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
