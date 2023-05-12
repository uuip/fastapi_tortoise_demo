import typing

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

if typing.TYPE_CHECKING:
    from .base import ERR


class BizException(Exception):
    # Business Exception，指业务代码
    err: "ERR"

    def __init__(self, err: "ERR", *args: object) -> None:
        super().__init__(*args)
        self.err = err

    @classmethod
    def handler(cls, request: Request, exc: "BizException") -> Response:
        return JSONResponse(exc.err.dict())

    @classmethod
    def register(cls, app: FastAPI):
        app.add_exception_handler(cls, cls.handler)
