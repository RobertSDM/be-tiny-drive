from gotrue.errors import AuthApiError
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import Session
from server.app.core.exceptions import (
    AccountAlreadyExists,
    AccountRegistrationError,
    DomainError,
    WrongAuthData,
)
from server.app.core.interfaces.AuthenticationInterface import AuthenticationInterface
from server.app.core.schemas import RefreshSessionData
from server.app.database.models.UserAccount import UserAccount
from server.app.database.repositories.account_repo import (
    account_by_email,
    account_save,
)


class AuthenticationService:

    def __init__(self, auth_client: AuthenticationInterface):
        self.auth_client = auth_client

    def login(self, email: str, password: str):
        try:
            return self.auth_client.login(email, password)
        except AuthApiError:
            raise WrongAuthData()

    def refresh_session(self, token: str) -> RefreshSessionData:
        try:
            return self.auth_client.refresh(token)
        except AuthApiError:
            raise DomainError("Error refreshing the session", 500)

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

        try:
            return account_save(db, account)
        except InvalidRequestError:
            self.auth_client.delete(resp.id)

    def logout(self, jwt: str):
        try:
            return self.auth_client.logout(jwt)
        except AuthApiError:
            raise DomainError("Error loging out the user", 500)
