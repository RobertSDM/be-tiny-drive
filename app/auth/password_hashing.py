import bcrypt


def hash_password(password: str, salt: str) -> str:
    return bcrypt.hashpw(
        password=password.encode(),
        salt=salt.encode(),
    ).decode()


def check_password_hash(db_pass: str, _pass: str) -> bool:
    return bcrypt.checkpw(_pass.encode(), db_pass.encode())
