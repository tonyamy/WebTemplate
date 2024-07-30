from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy_serializer import SerializerMixin

Base = declarative_base()
metadata = Base.metadata


class DbAccount(Base, SerializerMixin):
    __tablename__ = 'db_account'

    id = Column(Integer, primary_key=True)
    username = Column(String(255))
    password = Column(String(255))
    email = Column(String(255))
    role = Column(String(255))
    register_time = Column(DateTime)

# with session_scope() as session:
#     data, total = ModelCrud(session, DbAccount).paginate_query(filters=None, page=20)
#     # print(data)
#     print(total)
