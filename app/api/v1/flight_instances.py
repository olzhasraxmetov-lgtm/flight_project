from fastapi import APIRouter

from app.core.dependencies import DBDep
from app.core.dependencies import admin_only
from app.schemas.seat_instanes_map import FlightInstanceMapResponse
from app.services.flight_instances import FlightInstancesService
from app.schemas.flight_instances import FlightInstanceCreate, FlightInstanceResponse
router = APIRouter(
    prefix="/flight_instances",
    tags=["Вылеты по шаблону"]
)

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
    response_model=list[FlightInstanceMapResponse],
)
async def get_flight_instance_map(db: DBDep, instance_id: int):
    return await FlightInstancesService(db).get_flight_instance_map(instance_id)