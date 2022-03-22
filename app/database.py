from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


SQLALCHEMY_DATABASE_URL = f'mysql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Creating a Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Connection to database established using PyMySql
# while True:
#    try:
#        con = pymysql.connect(host='localhost', user='root', password='Bb228626!', database='fcc_schema',
#                              cursorclass=pymysql.cursors.DictCursor)
#        cursor = con.cursor()
#        print("Connection to Database was successful...")
#        break
#    except Exception as error:
#        print("Connection not successfully, database failed.")
#        print("Error: ", error)
#        time.sleep(4)
#  These will be the import needed in case you want to use RAW SQL instead of SQL ALCHEMY
#  import pymysql.cursors
#  import time
