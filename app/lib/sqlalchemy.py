import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.core.constants import DATABASE_URL


class SQLAlchemyClient:
    def __init__(self, conn_str: str):
        self.engine = sa.create_engine(conn_str)
        self.session_maker = sessionmaker(self.engine)

    def get_session(self):
        session = self.session_maker()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()


class Base(DeclarativeBase):
    pass


client = SQLAlchemyClient(DATABASE_URL)
