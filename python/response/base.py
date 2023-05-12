from typing import Optional

from pydantic import BaseModel

from .exceptions import BizException
from .generic import R, T


class ERR(BaseModel):
    code: int
    msg: str

    __all = dict()

    def throw(self):
        """根据该错误码抛出一个异常交给上游捕获，相当于直接返回这个对象

        Raises:
            BizException: [description]
        """
        raise BizException(self)

    @classmethod
    def register(cls, code: int, msg: str) -> "ERR":
        """注册一组code、msg为一个错误对象
        每个错误码原则上只对应一个错误，因此不同错误应该对应不同的code，避免歧义

        Raises:
            Exception: 错误码已经使用

        Returns:
            ERR: 注册成功的新错误
        """
        if code in cls.__all:
            raise Exception(f"错误码{code}已经注册为{cls.__all[code]}")
        err = cls(code=code, msg=msg)
        cls.__all[code] = err
        return err

    def inherit(self, msg: str):
        """
        生成一个新的错误，并修改错误信息为制定字符串。生成的对象应该只使用一次。

        >>> OK.inherit("上传成功")

        Args:
            msg (str): 新的错误描述

        Returns:
            ERR : 新的错误对象
        """
        return ERR(code=self.code, msg=msg)

    def __call__(self, data: Optional[T] = None) -> R[T]:
        """这个方法是依据错误类型，生成一个标准返回对象的快捷方法
        >>> ERROR("hello")

        等价于

        >>> R(data="hello",code=ERROR.code,msg=ERROR.msg)

        Args:
            data (Optional[T], optional): 返回对象的data. Defaults to None.

        Returns:
            R[T]: 生成的返回对象
        """
        return R(data=data, code=self.code, msg=self.msg)
