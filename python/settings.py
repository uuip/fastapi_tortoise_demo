from pathlib import Path

from pydantic import Field
from pydantic_settings import SettingsConfigDict, BaseSettings

_env_file = Path(__file__).parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=_env_file, extra="ignore")

    db: str = Field(alias="db_url")


settings = Settings()
