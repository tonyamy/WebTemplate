from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel, Session, select

from Service.Engine import engine

SQLModel.metadata.create_all(engine)


class DbAccount(SQLModel, table=True):
    __tablename__ = 'db_account'
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    password: str
    email: str
    role: str
    register_time: datetime


def aaa(page, size, filters=None):
    with Session(engine) as session:

        s = select(DbAccount).offset((page - 1) * size).limit(size)
        print(s)
        result = session.exec(s).all()

        print(len(result))
        print(result)
    return result


print(aaa(1, 10))
