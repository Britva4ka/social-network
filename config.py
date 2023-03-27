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