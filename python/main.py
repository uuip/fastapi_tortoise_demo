import logging
import os
import time

import uvicorn
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import BaseORMException

from api import data_api
from response import ERROR, PARAM_ERROR
from response.exceptions import BizException
from settings import settings
from utils import custom_openapi

app = FastAPI(title="demo project")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/time")
async def gettime() -> int:
    return int(time.time())


@app.on_event("startup")
async def startup_event():
    ...


@app.on_event("shutdown")
async def shutdown_event():
    ...


@app.exception_handler(RequestValidationError)
async def handle_params_error(requset: Request, exc: RequestValidationError):
    detail = "; ".join([get_exc_loc(x["loc"]) + ": " + x["msg"] for x in exc.errors()])
    return JSONResponse(jsonable_encoder(PARAM_ERROR(detail)))


@app.exception_handler(BaseORMException)
async def handle_orm_error(request: Request, exc: BaseORMException):
    return JSONResponse(jsonable_encoder(ERROR(exc.args)))


BizException.register(app)
app.include_router(data_api)
app.openapi = custom_openapi(app)

register_tortoise(
    app,
    db_url=settings.db,
    modules={"models": ["models"]},
    generate_schemas=False,
    # config={
    #         'apps'       : {'models': {'models': ["models"]}},
    #         'connections': {
    #                 'default': {
    #                         'engine'     : 'tortoise.backends.asyncpg',
    #                         'credentials': settings.db_dict,
    #                         'maxsize'    : 10,
    #                         }
    #                 }
    #         }
)


def get_exc_loc(info: tuple) -> str:
    if len(info) > 1:
        return info[1]
    else:
        return info[0]


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8003,
        reload=False,
        workers=os.cpu_count(),
        loop="uvloop",
        log_level=logging.ERROR,
    )
