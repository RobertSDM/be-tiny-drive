# from database.init_database import engine
# from database.model.user_model import Base

from database.init_database import engine
from database.model.user_model import Base


def db_push():
    Base.metadata.create_all(bind=engine)


db_push()
