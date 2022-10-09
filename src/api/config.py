from functools import cache

from pydantic import BaseSettings, Field


class Secrets(BaseSettings):
    app_name: str = "Ionite API"
    # api_key: str = Field(..., env='my_api_key')


@cache
def get_secrets() -> Secrets:
    return Secrets()
