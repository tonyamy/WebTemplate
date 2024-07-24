from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class DbAccount(Base):
    __tablename__ = 'db_account'

    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    password = Column(String(255))
    email = Column(String(255))
    role = Column(String(255))
    register_time = Column(DateTime)

    def __init__(self, Session):
        self.session = Session

    @classmethod
    def read(cls, session, account_id):
        return session.query(cls).filter_by(id=account_id).first()



