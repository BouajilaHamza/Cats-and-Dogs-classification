from decouple import config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    THE_CAT_API_KEY: str = config("THE_CAT_API_KEY")
    THE_DOG_API_KEY: str = config("THE_DOG_API_KEY")
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"



settings = Settings()