from typing import Self, Any

from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse

from .generic import ErrResponse


class ApiException(Exception):
    def __init__(self, err: ErrResponse, *args: Any) -> None:
        # err是ErrResponse实例，注册异常handler后，调用model_dump
        # ERROR = ErrResponse.register(400, "请求错误")
        # raise ApiException(ERROR)
        # raise ApiException(ERROR.excinfo("other info"))
        super().__init__(*args)
        self.err = err

    @classmethod
    def handler(cls, request: Request, exc: Self) -> Response:
        return JSONResponse(exc.err.model_dump())

    @classmethod
    def register(cls, app: FastAPI):
        app.add_exception_handler(cls, cls.handler)
