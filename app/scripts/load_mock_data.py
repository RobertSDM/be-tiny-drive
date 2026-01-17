from app.lib.sqlalchemy import client
from app.database.models.UserAccount import UserAccount

session = next(client.get_session())
account = UserAccount(
    id="3acd40a6-f384-4e34-8f95-476a0dec91a6",
    username="TestMockUserDatabaseApp",
    email="test@gmail.com",
    created_at="2025-05-27T13:51:34.116Z",
    
)
session.add(account)
session.commit()
