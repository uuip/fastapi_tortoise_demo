from datetime import datetime, timezone, timedelta

from pydantic import BaseModel as _BaseModel, validator

from models import User_Schema, Tree_Schema

sh = timezone(timedelta(hours=+8))


def transform_time(dt):
    return dt.astimezone(sh).strftime("%Y-%m-%d %H:%M:%S +08:00")


def transform_naive_time(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


class BaseModel(_BaseModel):
    class Config:
        orm_mode = True


class TreeSchema(Tree_Schema):
    @validator("create_at", "update_at")
    def transform_time(cls, v):
        if isinstance(v, int):
            v = datetime.fromtimestamp(v)
            return transform_naive_time(v)
        if isinstance(v, datetime):
            return transform_naive_time(v)
        return v


class UserSchema(User_Schema):
    ...


class Item(BaseModel):
    id: int
    energy: int
