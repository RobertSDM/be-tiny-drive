import bcrypt as bc

def encoder(_pass: str, salt: str) -> str:

    hashed_pass = bc.hashpw(
        password=_pass.encode(),
        salt=salt.encode(),
    ).decode()

    return hashed_pass


def validate_login(db_pass: str, _pass: str) -> bool:
    return bc.checkpw(_pass.encode(), db_pass.encode())
