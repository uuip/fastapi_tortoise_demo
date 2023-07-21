from datetime import datetime, timezone, timedelta

from pydantic import (
    BaseModel as _BaseModel,
    field_validator,
    ConfigDict,
    field_serializer,
    computed_field,
)

from models import User_Schema, Tree_Schema

sh = timezone(timedelta(hours=+8))


def transform_time(dt):
    return dt.astimezone(sh).strftime("%Y-%m-%d %H:%M:%S +08:00")


def transform_naive_time(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


class BaseModel(_BaseModel):
    model_config = ConfigDict(from_attributes=True)


class TreeSchema(Tree_Schema):
    @field_validator("created_at", "updated_at", mode="before")
    def transform_time(cls, v):
        if isinstance(v, int):
            v = datetime.fromtimestamp(v)
        return v

    @field_serializer("created_at", "updated_at")
    def serializes_time(self, v):
        return transform_naive_time(v)

    @computed_field(return_type=int)
    @property
    def someattr(self):
        return self.created_at.year


class UserSchema(User_Schema):
    ...


class Item(BaseModel):
    id: int
    energy: int
