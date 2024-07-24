import os
from contextlib import contextmanager

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

load_dotenv()
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
# echo 是打印 sql 查询语句
engine = create_engine(f'mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}', pool_size=10,
                       max_overflow=20,
                       pool_recycle=3600)

Base = declarative_base()
metadata = Base.metadata

Session = scoped_session(sessionmaker(bind=engine))


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    try:
        yield Session
        Session.commit()
    except:
        Session.rollback()
        raise
    finally:
        Session.remove()
