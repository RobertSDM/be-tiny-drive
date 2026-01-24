from sqlalchemy.orm import Session
from app.core.exceptions import AccountAlreadyExists, AccountRegistrationError
from app.database.models.UserAccount import UserAccount
from app.database.repositories.account_repo import (
    account_by_email,
    account_save,
)
from app.interfaces.authentication_interface import AuthenticationInterface


class AuthenticationService:

    def __init__(self, auth_client: AuthenticationInterface):
        self.auth_client = auth_client

    def register(
        self, db: Session, username: str, email: str, password: str
    ) -> UserAccount:
        exists = db.query(account_by_email(db, email).exists()).scalar()

        if exists:
            raise AccountAlreadyExists()

        resp = self.auth_client.register(email, password, username)
        if not resp:
            return AccountRegistrationError()

        account = UserAccount(
            id=resp.id,
            username=username,
            email=resp.email,
            created_at=resp.created_at,
        )

        return account_save(db, account)
