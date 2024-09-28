import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, sessionmaker
import dotenv

from project.variables.env_definitions import Database_url

dotenv.load_dotenv()

engine = sa.create_engine(
    Database_url, pool_pre_ping=True, pool_size=5, pool_recycle=3600, pool_timeout=30
)

Base = declarative_base()
__Session = sessionmaker(engine)


def get_session():
    session = __Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()
