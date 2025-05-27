from app.database.client.sqlalchemy_client import db_client
from app.database.models.account_model import Account

session = next(db_client.get_session())

account = Account(
    id="3acd40a6-f384-4e34-8f95-476a0dec91a6",
    username="TestMockUserDatabaseApp",
    email="test@gmail.com",
    creation_date="2025-05-27T13:51:34.116Z",
)
session.add(account)
session.commit()
