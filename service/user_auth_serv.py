import bcrypt
from sqlalchemy.orm import Session
from controller.auth import authenticate_token, create_token
from controller.convert_data import convert_user_to_response_user
from database.repository.UserRepository import (
    find_user_by_email,
    find_user_by_id,
    insert_user,
)
from database.schemas.schemas import DefaultDefReponse, UserParamRegisterSchema
from controller.pass_hashing import encoder, validate_login


def log_user_serv(db: Session, email: str, _pass: str) -> DefaultDefReponse:
    user = find_user_by_email(db, email)

    if not user:
        return {
            "status": 404,
            "content": {"msg": "The email or password is incorrect", "data": None},
        }

    if user.email != email:
        return {
            "status": 404,
            "content": {"msg": "The email or password is incorrect", "data": None},
        }

    isValid = validate_login(user.password, _pass)

    if not isValid:
        return {
            "status": 422,
            "content": {"msg": "The email or password is incorrect", "data": None},
        }

    token = create_token(user.id)

    return {
        "status": 200,
        "content": {
            "msg": "Success",
            "data": {
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "user_name": user.user_name,
                },
                "token": token,
            },
        },
    }


def pass_hashing_serv(db: Session, user: UserParamRegisterSchema):
    salt = bcrypt.gensalt().decode()

    user.password = encoder(user.password, salt)

    res = insert_user(db, user, salt)

    if not res:
        return {
            "status": 200,
            "content": {"msg": "Error while creating the user", "data": None},
        }

    return {"status": 200, "content": {"msg": "Success", "data": None}}


def validate_token_serv(db: Session, token: str):
    userId = authenticate_token(token)

    if not isinstance(userId, str):
        return userId

    userExist = find_user_by_id(db, userId)

    if not userExist:
        return {"status": 200, "content": {"msg": "The token is invalid", "data": None}}

    return True
