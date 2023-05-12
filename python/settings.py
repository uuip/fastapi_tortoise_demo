from typing import Optional
from urllib.parse import urlparse

from pydantic import root_validator, BaseSettings, Field, PostgresDsn


# from pydantic import Json,RedisDsn,HttpUrl,EmailStr
# from ipaddress import IPv4Address
# from pathlib import Path


class Settings(BaseSettings):
    db: PostgresDsn = Field(..., env="db")
    db_dict: Optional[dict]
    db_django: Optional[dict]

    @root_validator(pre=False)
    def set_variant(cls, values: dict):
        c = urlparse(values["db"])
        values["db_dict"] = {
                "host"    : c.hostname,
                "port"    : c.port or 5432,
                "database": c.path.lstrip("/"),
                "user"    : c.username,
                "password": c.password,
                }

        values["db_django"] = {
                "ENGINE"  : "django.db.backends.postgresql",
                "NAME"    : c.path.lstrip("/"),
                "USER"    : c.username,
                "PASSWORD": c.password,
                "HOST"    : c.hostname,
                "PORT"    : c.port or 5432,
                }
        return values

    class Config:
        env_file = ".env"


settings = Settings()
