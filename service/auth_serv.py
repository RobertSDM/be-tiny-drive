import bcrypt
from sqlalchemy.orm import Session
from database.models import User
from auth.jwt import authenticate_token, create_token
from database.repositories.user_repository import (
    user_by_email,
    user_by_id,
    user_create,
    user_exists_by_email,
)
from schemas.schemas import DefaultDefReponse, UserParamRegisterSchema
from service.item_serv import create_root_item
from auth.password_hashing import hash_password, check_password_hash


def login_serv(db: Session, email: str, _pass: str) -> DefaultDefReponse:
    user = user_by_email(db, email)

    if not user or user.email != email:
        return {
            "status": 400,
            "content": {"msg": "The email or password is incorrect", "data": None},
        }

    isValid = check_password_hash(user.password, _pass)

    if not isValid:
        return {
            "status": 400,
            "content": {"msg": "The email or password is incorrect", "data": None},
        }

    token = create_token(user.id)

    return {
        "status": 200,
        "content": {
            "msg": "Success",
            "token": token,
            "data": {
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "user_name": user.username,
                }
            },
        },
    }


def register_serv(db: Session, username: str, email: str, password: str) -> User | None:
    userexists = user_exists_by_email(db, email)

    if userexists:
        return None

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
