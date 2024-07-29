from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255, 'utf8mb3_bin'))
    password = Column(String(255, 'utf8mb3_bin'))
    nickname = Column(String(255, 'utf8mb3_bin'))
    roles = Column(String(255, 'utf8mb3_bin'))

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
