import jwt, dotenv
import jwt.algorithms
from service.logging_config import logger
from utils.env_definitions import Secret_key

dotenv.load_dotenv()

key = Secret_key


def create_token(userId: str):

    return jwt.encode(
        {"userId": str(userId)},
        key=key,
        algorithm="HS256",
    )


def authenticate_token(raw_token: str):
    token = __separate_token(raw_token)

    try:
        decoded = jwt.decode(token, key=key, algorithms="HS256")

        return decoded["userId"]
    except jwt.InvalidTokenError as e:
        logger.info(e)
        return {"status": 200, "content": {"msg": "The token is invalid", "data": None}}
    except jwt.ExpiredSignatureError as e:
        return {"status": 200, "content": {"msg": "The token is expired", "data": None}}


def __separate_token(raw_token: str):
    return raw_token.replace("bearer ", "")
