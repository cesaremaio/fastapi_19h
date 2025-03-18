from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import Settings

settings = Settings()
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal() # this is responsible for database interaction
    try:
        yield db
    finally:
        db.close()

# def connect_to_postgres():
#     ''' psycopg2 connects to postgres directly. Not needed with sqlalchemy.
#         Usage:
#             in main: 
#                 from . import database
#                 database.connect_to_postgres() 
#     '''
#     import psycopg2
#     from loguru import logger
#     import time
#     try:
#         conn = psycopg2.connect(host="localhost", 
#                                 database="mydatabase",
#                                 user="postgres",
#                                 password="password123",
#                                 port=5432, )
#         cursor = conn.cursor()
#         logger.debug(f'Database connection successful.'),

#     except Exception as e:
#         logger.debug(f'Database connection failed.')
#         logger.debug(f'Error: {e}')
#         time.sleep(2)

