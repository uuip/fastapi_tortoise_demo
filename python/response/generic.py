from typing import Generic, Optional, TypeVar, ClassVar, Self

from pydantic import BaseModel
from pydantic.fields import Field

T = TypeVar("T")


class R(BaseModel, Generic[T]):
    code: int = Field(200, description="response code")
    msg: str = Field("success", description="response description message")
    data: Optional[T] = Field(None, description="response data")


class ErrResponse(BaseModel):
    code: int
    msg: str

    __all: ClassVar = dict()

    @classmethod
    def register(cls, code: int, msg: str) -> Self:
        """注册一组code、msg为一个错误对象"""
        if code in cls.__all:
            raise Exception(f"错误码{code}已经注册为{cls.__all[code]}")
        err = cls(code=code, msg=msg)
        cls.__all[code] = err
        return err

    def excinfo(self, msg: str) -> Self:
        """
        基于已注册错误对象生成一个新的错误，并修改错误信息为制定字符串。
        """
        return ErrResponse(code=self.code, msg=msg)

    def __call__(self, data: Optional[T] = None) -> R[T]:
        return R(data=data, code=self.code, msg=self.msg)
