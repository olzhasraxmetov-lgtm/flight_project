from fastapi import APIRouter

from app.core.dependencies import DBDep
from app.core.dependencies import admin_only
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
