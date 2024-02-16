from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from backend_server.config import config

db_engine = create_engine(config.mysql_url.unicode_string())
db_session = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)


Base = declarative_base()


def get_db():
    with db_session() as session:
        yield session
