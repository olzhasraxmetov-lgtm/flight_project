from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.core.dependencies import DBDep
from app.core.dependencies import admin_only
from app.services.aircrafts import AircraftsService
from app.schemas.aircrafts import AircraftResponse, AircraftCreate, AircraftUpdate

router = APIRouter(
    prefix="/aircrafts",
    tags=["Самолеты"]
)

@router.post(
    "",
    response_model=AircraftResponse,
    summary='Создать новый самолет',
    dependencies=[admin_only]
)
async def create_aircraft(
    db: DBDep,
    payload: AircraftCreate
):
    return await AircraftsService(db).create_aircraft(payload)

@router.get(
    "",
    response_model=list[AircraftResponse],
    summary='Получить все самолеты',
    dependencies=[admin_only]
)
@cache(expire=60)
async def get_all_aircrafts(
    db: DBDep
):
    return await AircraftsService(db).get_aircrafts()

@router.get(
    "/{aircraft_id}",
    response_model=AircraftResponse,
    summary='Получить самолет по ID',
    dependencies=[admin_only]
)
async def get_aircraft_by_id(
    db: DBDep,
    aircraft_id: int
):
    return await AircraftsService(db).get_aircraft_by_id(aircraft_id)

@router.put(
    "/{aircraft_id}",
    response_model=AircraftResponse,
    summary='Обновить самолет по ID',
    dependencies=[admin_only]
)
async def update_aircraft(
    db: DBDep,
    payload: AircraftUpdate,
    aircraft_id: int
):
    return await AircraftsService(db).update_aircraft(aircraft_id=aircraft_id, payload=payload)

@router.patch(
    "/{aircraft_id}",
    response_model=AircraftResponse,
    summary='Частично обновить самолет по ID',
    dependencies=[admin_only]
)
async def partially_update_aircraft(
    db: DBDep,
    payload: AircraftUpdate,
    aircraft_id: int
):
    return await AircraftsService(db).partially_update_aircraft(aircraft_id=aircraft_id, payload=payload)

@router.delete(
    "/{aircraft_id}",
    summary='Удалить самолет по ID',
    dependencies=[admin_only],
    status_code=204,
)
async def delete_aircraft(
    db: DBDep,
    aircraft_id: int
):
    return await AircraftsService(db).delete_aircraft(aircraft_id=aircraft_id)