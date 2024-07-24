import os

from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    generateCommand = (f" sqlacodegen mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@"
                       f"{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}")
    print(generateCommand)
