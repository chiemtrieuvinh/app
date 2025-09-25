import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

def get_database_url():
    engine = os.environ.get("DB_ENGINE")
    username = os.environ.get("DB_USERNAME")
    password = os.environ.get("DB_PASSWORD")
    host = os.environ.get("DB_HOST")
    port = os.environ.get("DB_PORT")
    dbname = os.environ.get("DB_NAME")
    return f"{engine}://{username}:{password}@{host}:{port}/{dbname}"

# Database setting
SQLALCHEMY_DATABASE_URL = get_database_url()
ADMIN_DEFAULT_PASSWORD = os.environ.get("DEFAULT_PASSWORD")


#JWT setting
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")

