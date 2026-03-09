from fastapi import APIRouter, Body, Response

from app.core.dependencies import CurrentUser, admin_only
from app.core.dependencies import DBDep
from app.schemas.airports import AirportResponse, AirportCreate, AirportUpdate
from app.services.airports import AirportsService
from app.exceptions.base import AirportNotFoundException
from app.exceptions.api import AirportNotFoundHTTPException
router = APIRouter(
    prefix="/airports",
    tags=["Аэропорты"],
)

@router.get("", response_model=list[AirportResponse], summary='Получить список аэропортов')
async def get_airports(
    db: DBDep,
):
    return await AirportsService(db).get_airports()

@router.post(
    "",
     response_model=AirportResponse,
     summary='Добавить новый аэропорт',
     dependencies=[admin_only]
)
async def create_airport(
        db: DBDep,
        payload: AirportCreate,
):
    return await AirportsService(db).create_airport(payload)

@router.get("/{airport_id}", response_model=AirportResponse, summary='Получить аэропорт по ID')
async def get_airport_by_id(
    db: DBDep,
    airport_id: int
):
    try:
        return await AirportsService(db).get_airport_by_id(airport_id)
    except AirportNotFoundException:
        raise AirportNotFoundHTTPException

@router.put(
    "/{airport_id}",
    response_model=AirportResponse,
    summary='Обновить аэропорт',
    dependencies=[admin_only]
)
async def update_airport(
        db: DBDep,
        airport_id: int,
        payload: AirportUpdate,
):
    try:
        return await AirportsService(db).update_airline(payload=payload, airport_id=airport_id)
    except AirportNotFoundException:
        raise AirportNotFoundHTTPException

@router.patch(
    "/{airport_id}",
    response_model=AirportResponse,
    summary='Частично обновить аэропорт',
    dependencies=[admin_only]
)
async def partially_update_airport(
        db: DBDep,
        airport_id: int,
        payload: AirportUpdate,
):
    try:
        return await AirportsService(db).partially_update_airline(payload=payload, airport_id=airport_id)
    except AirportNotFoundException:
        raise AirportNotFoundHTTPException

@router.delete(
    "/{airport_id}",
    summary='Удалить аэропорт',
    status_code=204,
    dependencies=[admin_only]
)
async def delete_airport(
        db: DBDep,
        airport_id: int
):
    try:
        return await AirportsService(db).delete_airport(airport_id)
    except AirportNotFoundException:
        raise AirportNotFoundHTTPException