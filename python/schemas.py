from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import (
    BaseModel,
    field_validator,
    ConfigDict,
    field_serializer,
    computed_field,
)

sh = ZoneInfo("Asia/Shanghai")


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime

    # mode="before"：输入数据转换为字段前验证，after则是转换后再验证。函数第一个参数cls
    @field_validator("created_at", "updated_at", mode="before")
    def transform_time(cls, v):
        if isinstance(v, int):
            v = datetime.fromtimestamp(v)
        return v

    @field_serializer("created_at", "updated_at")
    def serializes_time(self, v):
        return v.strftime("%Y-%m-%d %H:%M:%S")


class TreeSchema(BaseSchema):
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
