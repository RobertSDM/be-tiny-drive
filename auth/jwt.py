import jwt, dotenv
from datetime import datetime, timedelta
import jwt.algorithms
from utils.logging_config import logger
from constants.env_definitions import secret_key, clients_URL

dotenv.load_dotenv()

access_token = secret_key


def create_token(userId: str):
    return jwt.encode(
        {
            "userId": str(userId),
            "exp": datetime.now() + timedelta(weeks=2),
            "nbf": datetime.now(),
            "iss": "bk-tiny-drive.azurewebsites.net",
            "aud": [i for i in clients_URL.split(";")],
            "iat": datetime.now(),
        },
        key=access_token,
        algorithm="HS256",
    )


def authenticate_token(raw_token: str):
    token = __separate_token(raw_token)

    try:
        decoded = jwt.decode(
            token,
            key=access_token,
            algorithms="HS256",
            issuer="bk-tiny-drive.azurewebsites.net",
            audience=[i for i in clients_URL.split(";")],
        )

        return decoded["userId"]
    except jwt.InvalidTokenError as e:
        logger.info(e)
        return {"status": 200, "content": {"msg": "The token is invalid", "data": None}}
    except jwt.ExpiredSignatureError as e:
        return {"status": 200, "content": {"msg": "The token is expired", "data": None}}


def __separate_token(raw_token: str):
    return raw_token.replace("bearer ", "")
