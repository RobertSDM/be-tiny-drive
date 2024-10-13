import bcrypt
from sqlalchemy.orm import Session
from security.jwt.auth import authenticate_token, create_token
from database.repository.user_repository import (
    find_user_by_email,
    find_user_by_id,
    insert_user,
)
from database.schemas import DefaultDefReponse, UserParamRegisterSchema
from utils.pass_hashing import encoder, validate_login


def log_user_serv(db: Session, email: str, _pass: str) -> DefaultDefReponse:
    user = find_user_by_email(db, email)

    if not user or user.email != email:
        return {
            "status": 400,
            "content": {"msg": "The email or password is incorrect", "data": None},
        }

    isValid = validate_login(user.password, _pass)

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
                    "user_name": user.user_name,
                }
            },
        },
    }


def register_serv(db: Session, p_user: UserParamRegisterSchema):
    user = find_user_by_email(db, p_user.email)

    if user:
        return {
            "status": 400,
            "content": {"msg": "The user with the email already exist", "data": None},
        }

    salt = bcrypt.gensalt().decode()

    p_user.password = encoder(p_user.password, salt)

    res = insert_user(db, p_user, salt)

    if not res:
        return {
            "status": 500,
            "content": {"msg": "Error while creating the user", "data": None},
        }

    return {"status": 200, "content": {"msg": "Success", "data": None}}


def __cut_header_token(header_token: str) -> str:
    return header_token.replace("Bearer ", "")


def validate_token_serv(db: Session, header_token: str):
    token = __cut_header_token(header_token)

    userId = authenticate_token(token)

    if not isinstance(userId, str):
        return userId

    userExist = find_user_by_id(db, userId)

    if not userExist:
        return {"status": 200, "content": {"msg": "The token is invalid", "data": None}}

    return True
