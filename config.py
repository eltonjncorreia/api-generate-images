from functools import lru_cache
import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Gerador de imagens por OpenAI API"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
