from fastapi import APIRouter, Depends

from app.core.dependencies import DBDep, PaginationDep
from app.core.dependencies import admin_only
from app.schemas.flights import FlightSearch
from app.schemas.seat_instanes_map import FlightInstanceMapResponse
from app.services.flight_instances import FlightInstancesService
from app.schemas.flight_instances import FlightInstanceCreate, FlightInstanceResponse, FlightInstanceStatusUpdate

router = APIRouter(
    prefix="/flight_instances",
    tags=["Вылеты по шаблону"]
)

@router.get(
    "",
    summary='Получить все рейсы',
    response_model=list[FlightInstanceResponse],
)
async def get_paginated_flight_instances(
        db: DBDep,
        pagination: PaginationDep,
        search_params: FlightSearch = Depends(),
):
    return await FlightInstancesService(db).get_paginated_flight_instances(search_params, pagination)


@router.post(
    "",
    summary='Создать вылет по расписанию',
    dependencies=[admin_only],
    response_model=FlightInstanceResponse
)
async def create_flight_instance(
    db: DBDep,
    payload: FlightInstanceCreate,
):
    return await FlightInstancesService(db).create_flight_instance(payload)

@router.get(
    "/{instance_id}/seats",
    summary='Получить карту мест вылета по ID',
    response_model=FlightInstanceMapResponse,
)
async def get_flight_instance_map(db: DBDep, instance_id: int):
    return await FlightInstancesService(db).get_flight_instance_map(instance_id)

@router.patch(
    "/{instance_id}/status",
    summary='Изменить статус рейса',
    dependencies=[admin_only],
    response_model=FlightInstanceResponse
)
async def change_flight_instance_status(
        db: DBDep,
        instance_id: int,
        payload: FlightInstanceStatusUpdate
):
    return await FlightInstancesService(db).change_flight_instance_status(payload=payload, flight_instance_id=instance_id)