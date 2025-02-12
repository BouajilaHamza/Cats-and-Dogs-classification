from decouple import config
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Cats and Dogs Classification API"
    PROJECT_DESCRIPTION: str = "An API for classifying cat and dog images"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG_MODE: bool = True
    ALLOWED_ORIGINS: List[str] = ["*"]
    THE_CAT_API_KEY: str = config("THE_CAT_API_KEY", cast=str)
    THE_DOG_API_KEY: str = config("THE_DOG_API_KEY", cast=str)
    COMET_API_KEY: str = ""
    COMET_WORKSPACE: str = ""
    TRAIN_DIR: str = "app/data/training_set"
    VAL_DIR: str = "app/data/validation_set"
    BATCH_SIZE: int = 128
    EPOCHS: int = 5

    class Config:
        env_file = ".env"

settings = Settings()