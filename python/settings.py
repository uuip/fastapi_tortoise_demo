from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

from pydantic import Field, PostgresDsn, model_validator
from pydantic_settings import SettingsConfigDict, BaseSettings

# from pydantic import Json,RedisDsn,HttpUrl,EmailStr
# from ipaddress import IPv4Address
# from pathlib import Path

_env_file = Path(__file__).parent / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=_env_file, extra="ignore")

    db: PostgresDsn = Field(alias="db")
    db_dict: Optional[dict]
    db_django: Optional[dict]

    @model_validator(mode="before")
    def set_variant(cls, values: dict):
        c = urlparse(values["db"])
        values["db_dict"] = {
            "host": c.hostname,
            "port": c.port or 5432,
            "database": c.path.lstrip("/"),
            "user": c.username,
            "password": c.password,
        }

        values["db_django"] = {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": c.path.lstrip("/"),
            "USER": c.username,
            "PASSWORD": c.password,
            "HOST": c.hostname,
            "PORT": c.port or 5432,
        }
        return values


settings = Settings()
