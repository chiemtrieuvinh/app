import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
load_dotenv()

def get_connection_str():
    engine = os.getenv("DB_ENGINE")
    username = os.getenv("DB_USERNAME")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    table = os.getenv("DB_NAME")
    return f"{engine}://{username}:{password}@{host}:{port}/{table}"

print(get_connection_str())
SQLALCHEMY_DATABASE_URL = get_connection_str()

engine = create_engine(SQLALCHEMY_DATABASE_URL)
metadata = MetaData()

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()

def get_db_context():
    try:
        db = LocalSession()
        yield db
    finally:
        db.close()