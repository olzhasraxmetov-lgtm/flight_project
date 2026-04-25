from fastapi import APIRouter, Depends
from fastapi_cache.decorator import cache

from app.core.dependencies import DBDep
from app.core.dependencies import admin_only, PaginationDep
from app.schemas.flights import FlightCreate, FlightResponse, FlightUpdate, FlightResponseWithoutRels, FlightSearch
from app.services.flights import FlightsService

router = APIRouter(
    prefix="/flights",
    tags=["Вылеты"],
)

@router.get('', summary='Получить список вылетов',dependencies=[admin_only], response_model=list[FlightResponse])
@cache(expire=60)
async def get_paginated_flights(
    db: DBDep,
    pagination: PaginationDep,
    search_params: FlightSearch = Depends(),
):
    return await FlightsService(db).get_paginated_flights(search_params, pagination)

@router.post('', summary='Создать новый вылет', dependencies=[admin_only], response_model=FlightResponse)
async def create_flight(
        db: DBDep,
        payload: FlightCreate
):
    return await FlightsService(db).create_flight(payload)

@router.get('/{flight_id}', summary='Получить рейс по ID', dependencies=[admin_only], response_model=FlightResponse)
async def get_flight_by_id(
        db: DBDep,
        flight_id: int,
):
    return await FlightsService(db).get_flight(flight_id)

@router.delete('/{flight_id}', summary='Удалить рейс по ID', dependencies=[admin_only], status_code=204)
async def delete_flight_by_id(
        db: DBDep,
        flight_id: int,
):
    return await FlightsService(db).delete_flight(flight_id)

@router.put(
    '/{flight_id}',
        summary='Обновить рейс по ID',
        response_model=FlightResponseWithoutRels,
        dependencies=[admin_only]
)
async def update_flight_by_id(
        db: DBDep,
        flight_id: int,
        payload: FlightUpdate,
):
    return await FlightsService(db).update_flight(flight_id=flight_id, payload=payload)


@router.patch(
    '/{flight_id}',
        summary='Частично обновить рейс по ID',
        response_model=FlightResponseWithoutRels,
        dependencies=[admin_only]
)
async def partially_update_flight_by_id(
        db: DBDep,
        flight_id: int,
        payload: FlightUpdate,
):
    return await FlightsService(db).partially_update_flight(flight_id=flight_id, payload=payload)
