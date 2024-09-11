from pydantic_settings import BaseSettings


DB_SERVICE = "mysql+mysqlconnector"
DB_USERNAME = "test4321"
DB_PASSWORD = "test4321"
DB_HOST = "localhost"
DB_NAME = "test"

db_url = DB_SERVICE + "://" + DB_USERNAME + ":" + \
    DB_PASSWORD + "@" + DB_HOST + "/" + DB_NAME


class Settings(BaseSettings):
    # DATABASE_URL: str = "sqlite:///./test4.db"
    DATABASE_URL: str = db_url
    SECRET_KEY: str = "mySecretKey"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 24 * 60 * 7


settings = Settings()
