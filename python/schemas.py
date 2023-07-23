from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import (
    BaseModel as _BaseModel,
    field_validator,
    ConfigDict,
    field_serializer,
    computed_field,
)

sh = ZoneInfo("Asia/Shanghai")


def transform_time(dt):
    return dt.astimezone(sh).strftime("%Y-%m-%d %H:%M:%S +08:00")


def transform_naive_time(dt):
    return dt.strftime("%Y-%m-%d %H:%M:%S")


class BaseModel(_BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime

    @field_validator("created_at", "updated_at", mode="before")
    def transform_time(cls, v):
        if isinstance(v, int):
            v = datetime.fromtimestamp(v)
        return v

    @field_serializer("created_at", "updated_at")
    def serializes_time(self, v):
        return transform_naive_time(v)


class TreeSchema(BaseModel):
    name: str
    desc: str
    energy: int

    @computed_field(return_type=int)
    @property
    def someattr(self):
        return self.created_at.year


class Item(BaseModel):
    id: int
    energy: int
