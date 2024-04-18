import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')
db_host = os.getenv('DB_HOST')
# echo 是打印 sql 查询语句
engine = create_engine(f'mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}', pool_size=10,
                       max_overflow=20,
                       pool_recycle=3600)

