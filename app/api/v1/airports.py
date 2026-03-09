from fastapi import APIRouter, Body, Response

from app.core.dependencies import CurrentUser, admin_only
from app.core.dependencies import DBDep
from app.schemas.airports import AirportResponse, AirportCreate, AirportUpdate
from app.services.airports import AirportsService

router = APIRouter(
    prefix="/airports",
    tags=["Аэропорты"],
)

@router.get("", response_model=list[AirportResponse], summary='Получить список аэропортов')
async def get_airports():
    pass

@router.post(
    "",
     response_model=AirportResponse,
     summary='Добавить новый аэропорт',
     dependencies=[admin_only]
)
async def create_airport(
):
    pass

@router.get("/{airport_id}", response_model=AirportResponse, summary='Получить аэропорт по ID')
async def get_airport_by_id(
    airport_id: int
):
    pass

@router.put(
    "/{airport_id}",
    response_model=AirportResponse,
    summary='Обновить аэропорт',
    dependencies=[admin_only]
)
async def update_airport(
        airport_id: int
):
    pass

@router.patch(
    "/{airport_id}",
    response_model=AirportResponse,
    summary='Частично обновить аэропорт',
    dependencies=[admin_only]
)
async def partially_update_airport(
        airport_id: int
):
    pass

@router.delete(
    "/{airport_id}",
    summary='Удалить аэропорт',
    status_code=204,
    dependencies=[admin_only]
)
async def delete_airport(
        airport_id: int
):
    pass
