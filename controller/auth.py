import jwt, dotenv, os
import jwt.algorithms
from service.logging_config import logger

dotenv.load_dotenv()

key = os.environ.get("SECRET_KEY")


def create_token(userId: str):

    return jwt.encode(
        {
            "userId": str(userId),
        },
        key=key,
        algorithm="HS256",
    )


def authenticate_token(raw_token: str):
    token = __separate_token(raw_token)

    try:
        decoded = jwt.decode(token, key=key, algorithms="HS256")

        return decoded["userId"]
    except jwt.InvalidTokenError as e:
        logger(e)
        return {"status": 200, "content": {"msg": "The token is invalid", "data": None}}
    except jwt.ExpiredSignatureError as e:
        return {"status": 200, "content": {"msg": "The token is expired", "data": None}}

def __separate_token(raw_token: str):
    return raw_token.replace("bearer ", "")
