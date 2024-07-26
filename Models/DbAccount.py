from typing import Type, TypeVar, Optional, Generic

import sqlalchemy.orm.decl_api
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from Service.Engine import session_scope

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


T = TypeVar('T', bound=Base)


class ModelCrud(Generic[T]):

    def __init__(self, Session: Type[sqlalchemy.orm.scoping.scoped_session],
                 Model: Type[T]):
        # T = TypeVar('T', bound=Model)
        a = list[a]
        self.session = Session
        self.Model = Model

    def getById(self, Id: int) -> Optional[T]:
        return self.session.query(self.Model).filter_by(id=Id).first()


with session_scope() as session:
    a = ModelCrud(session, DbAccount)

# T = TypeVar('T', bound=DbAccount)
