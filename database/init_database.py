import sqlalchemy as sa
from sqlalchemy.orm import declarative_base, sessionmaker
import dotenv

from utils.env_definitions import Database_url

dotenv.load_dotenv()

engine = sa.create_engine(Database_url)

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
