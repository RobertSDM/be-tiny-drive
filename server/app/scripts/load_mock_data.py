from server.app.lib.sqlalchemy import client
from server.app.database.models.UserAccount import UserAccount

session = next(client.get_session())
account = UserAccount(
    id="7dc334cc-c103-4bd4-bdf4-dfc2a76f2f2d",
    username="TestMockUserDatabaseApp",
    email="test@gmail.com",
    created_at="2025-05-27T13:51:34.116Z",
)
session.add(account)
session.commit()
