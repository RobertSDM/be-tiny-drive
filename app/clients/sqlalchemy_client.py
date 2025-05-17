import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from app.constants.env_definitions import database_url
from app.interfaces.database_interface import DatabaseClientInterface


class SQLAlchemyClient(DatabaseClientInterface):
    def __init__(self, conn_str: str):
        self.engine = sa.create_engine(
            conn_str,
            pool_pre_ping=True,
            pool_size=5,
            pool_recycle=3600,
            pool_timeout=30,
        )
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


db_client = SQLAlchemyClient(database_url)
