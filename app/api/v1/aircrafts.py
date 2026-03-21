from fastapi import APIRouter

from app.core.dependencies import DBDep
from app.core.dependencies import admin_only
from app.services.aircrafts import AircraftsService
from app.schemas.aircrafts import AircraftResponse, AircraftCreate

router = APIRouter(
    prefix="/aircrafts",
    tags=["Самолеты"]
)

@router.post("", response_model=AircraftResponse, summary='Создать новый самолет', dependencies=[admin_only])
async def create_aircraft(
    db: DBDep,
    payload: AircraftCreate
):
    return await AircraftsService(db).create_aircraft(payload)

@router.get("", response_model=list[AircraftResponse], summary='Получить все самолеты', dependencies=[admin_only])
async def create_aircraft(
    db: DBDep
):
    return await AircraftsService(db).get_aircrafts()