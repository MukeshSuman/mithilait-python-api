from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

AZ_SPEECH_KEY = os.getenv('AZ_SPEECH_KEY', 'development')
AZ_SERVICE_REGION = os.getenv('AZ_SERVICE_REGION')

DB_SERVICE = os.getenv('DB_SERVICE')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

# DATABASE_URL: str = "sqlite:///./test.db"
db_url = "sqlite:///./test.db"
if DB_SERVICE is not None:
    db_url = DB_SERVICE + "://" + DB_USERNAME + ":" + \
        DB_PASSWORD + "@" + DB_HOST + "/" + DB_NAME


class Settings(BaseSettings):
    DATABASE_URL: str = db_url
    SECRET_KEY: str = "mySecretKey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 24 * 60 * 7
    AZ_SPEECH_KEY: str = AZ_SPEECH_KEY
    AZ_SERVICE_REGION: str = AZ_SERVICE_REGION


settings = Settings()
