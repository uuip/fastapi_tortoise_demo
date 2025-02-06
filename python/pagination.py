from typing import TypeVar, Generic, Sequence, Self

from pydantic import Field, BaseModel, conint
from tortoise.queryset import QuerySet

T = TypeVar("T")


class Pagination(BaseModel):
    page: int = Field(default=1, description="页码")
    size: int = Field(default=10, description="页面容量")


class Page(BaseModel, Generic[T]):
    code: int = 200
    page: conint(ge=1)
    size: conint(ge=1)
    total: conint(ge=0)
    data: Sequence[T]

    @classmethod
    async def create(cls, qs: QuerySet, pagination: Pagination) -> Self:
        size = pagination.size
        page = pagination.page
        # 大量数据时计算total，非常影响性能；total可以单独一个接口，查询一次即可
        return cls(
            total=0,
            data=await qs.limit(size).offset(page * size - size),
            page=page,
            size=size,
        )
