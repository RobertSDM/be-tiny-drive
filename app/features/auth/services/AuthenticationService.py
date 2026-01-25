from sqlalchemy.orm import Session
from supabase import SupabaseAuthClient
from app.core.exceptions import AccountAlreadyExists, AccountRegistrationError
from app.core.interfaces import AuthenticationInterface
from app.database.models.UserAccount import UserAccount
from app.database.repositories.account_repo import (
    account_by_email,
    account_save,
)


class AuthenticationService:

    def __init__(self, auth_client: AuthenticationInterface):
        self.auth_client = auth_client

    def login(self, email: str, password: str):
        return self.auth_client.login(email, password)

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

    def logout(self, jwt: str):
        return self.auth_client.logout(jwt)
