import os
from dotenv import load_dotenv


# load environment variables from .env
load_dotenv()


class Config:
    """
    Base configuration class
    """

    # read from .env file
    SECRET_KEY = os.getenv("SECRET_KEY")
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///network.db'

    POSTGRES_USER = os.getenv("USER")
    POSTGRES_PASSWORD = os.getenv("PASSWORD")
    POSTGRES_HOST = os.getenv("HOST")
    POSTGRES_DB = os.getenv("DB_NAME")
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
        POSTGRES_USER,
        POSTGRES_PASSWORD,
        POSTGRES_HOST,
        POSTGRES_DB
    )
    UPLOADED_PHOTOS_DEST = os.getenv("UPLOADED_PHOTOS_DEST")
    CSV_DATA_DEST = os.getenv("CSV_DATA_DEST")
