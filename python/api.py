import random

from fastapi import Query, APIRouter, Depends

from models import Trees
from pagination import Page, Pagination
from response import OK, R
from schemas import TreeSchema, Item

data_api = APIRouter(prefix="/tree", tags=["管理树木实体"])


@data_api.get("/q", response_model=Page[TreeSchema], summary="条件查询树木", )
async def query_trees(pagination: Pagination = Depends(), energy: int = Query(ge=0)):
    qs = Trees.filter(energy__gt=energy)
    return await Page.create(qs, pagination)


@data_api.get("/{id}", response_model=R[TreeSchema], response_model_by_alias=False, summary="查询单个树木")
async def query_tree(id: int):
    qs = await Trees.filter(id=id).first()
    return OK(qs)


@data_api.post("/update", response_model=R[TreeSchema], summary="更新单个树木信息")
async def update_tree(item: Item):
    obj = await Trees.filter(id=random.randint(1, 1000000)).first()
    obj.energy = item.energy
    await obj.save(update_fields=["energy"])
    # return JSONResponse(status_code=status.HTTP_201_CREATED, content=item)
    return OK(obj)
