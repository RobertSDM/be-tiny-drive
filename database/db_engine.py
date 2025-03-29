from contextlib import contextmanager
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from project.variables.env_definitions import database_url

engine = sa.create_engine(
    database_url, pool_pre_ping=True, pool_size=5, pool_recycle=3600, pool_timeout=30
)
session_maker = sessionmaker(engine)


class Base(DeclarativeBase):
    pass


def create_db():
    Base.metadata.create_all(engine)


@contextmanager
def get_session():
    session = session_maker()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
