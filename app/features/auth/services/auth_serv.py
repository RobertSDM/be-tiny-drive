from sqlalchemy.orm import Session
from app.core.exceptions import AccountAlreadyExists, AccountRegistrationError
from app.database.models.account_model import Account
from app.database.repositories.account_repo import (
    account_by_email,
    account_save,
)
from app.interfaces.authentication_interface import AuthenticationInterface
from app.utils.query import exec_exists


class AuthenticationService:

    def __init__(self, auth_client: AuthenticationInterface):
        self.auth_client = auth_client

    def register_serv(
        self, db: Session, username: str, email: str, password: str
    ) -> Account:
        exists = exec_exists(db, account_by_email(db, email))

        if exists:
            raise AccountAlreadyExists()

        resp = self.auth_client.registerPassword(email, password)
        if not resp:
            return AccountRegistrationError()

        account = Account(
            id=resp.id,
            username=username,
            email=resp.email,
            creation_date=resp.creation_date,
        )

        return account_save(db, account)
