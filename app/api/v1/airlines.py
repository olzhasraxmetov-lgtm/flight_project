from fastapi import APIRouter, Body, Query
from fastapi_cache.decorator import cache

from app.core.dependencies import DBDep
from app.core.dependencies import admin_only, PaginationDep
from app.exceptions.api import AirlineNotFoundHTTPException
from app.exceptions.base import AirlineNotFoundException
from app.schemas.airlines import AirlineResponse, AirlineCreate, AirlineUpdate
from app.services.airlines import AirlinesService

router = APIRouter(
    prefix="/airlines",
    tags=["Авиакомпаний"]
)

@router.get("/", response_model=list[AirlineResponse], summary='Получит список авиакомпаний')
@cache(expire=60)
async def get_airlines(
    db: DBDep,
    pagination: PaginationDep,
    name: str = Query(None, min_length=3, max_length=30, description='Название авиакомпаний'),
):
    return await AirlinesService(db).get_filtered_airlines_with_pagination(
        pagination=pagination,
        name=name,
    )


@router.get("/{airline_id}", summary='Получить авиакомпанию по ID', response_model=AirlineResponse)
async def get_airline(
    db: DBDep,
    airline_id: int,
):
    try:
        return await AirlinesService(db).get_airline(airline_id)
    except AirlineNotFoundException:
        raise AirlineNotFoundHTTPException

@router.post("/",
             summary='Добавить новую авиакомпанию',
             dependencies=[admin_only],
             response_model=AirlineResponse
)
async def create_airline(
    db: DBDep,
    payload: AirlineCreate = Body(...),
):
    return await AirlinesService(db).create_airline(payload=payload)



@router.put(
    "/{airline_id}",
    summary='Обновить авиакомпанию',
    dependencies=[admin_only],
    response_model=AirlineResponse
)
async def update_airlines(
    db: DBDep,
    airline_id: int,
    payload: AirlineUpdate = Body(...),
):
    try:
        return await AirlinesService(db).update_airline(payload=payload, airline_id=airline_id)
    except AirlineNotFoundException:
        raise AirlineNotFoundHTTPException


@router.patch(
    "/{airline_id}",
    summary='Частично обновить авиакомпанию',
    dependencies=[admin_only],
    response_model=AirlineResponse
)
async def update_airline(
    db: DBDep,
    airline_id: int,
    payload: AirlineUpdate = Body(...),
):
    try:
        return await AirlinesService(db).partially_update_airline(payload=payload, airline_id=airline_id)
    except AirlineNotFoundException:
        raise AirlineNotFoundHTTPException

@router.delete(
    "/{airline_id}",
    summary='Удалить авиакомпанию',
    dependencies=[admin_only],
    status_code=204,
)
async def delete_airlines(
    db: DBDep,
    airline_id: int,
):
    try:
        return await AirlinesService(db).delete_airline(airline_id=airline_id)
    except AirlineNotFoundException:
        raise AirlineNotFoundHTTPException