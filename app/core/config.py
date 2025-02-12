from decouple import config
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str  = "Cats And Dogs"
    PROJECT_DESCRIPTION: str = "Cats and Dogs classification project"
    VERSION: str = "1"
    API_V1_STR: str = "/api/v1"
    ALLOWED_ORIGINS: str = ""
    THE_CAT_API_KEY: str = config("THE_CAT_API_KEY" , cast=str)
    THE_DOG_API_KEY: str = config("THE_DOG_API_KEY" , cast=str)
    class Config:
        env_file = ".env"
        
settings = Settings()