from typing import Generic, Optional, TypeVar

from pydantic.fields import Field
from pydantic.generics import GenericModel

T = TypeVar("T")
TModel = TypeVar("TModel")


class R(GenericModel, Generic[T]):
    code: int = Field(200, description="response code")
    msg: str = Field("success", description="response description message")
    data: Optional[T] = Field(None, description="response data")
