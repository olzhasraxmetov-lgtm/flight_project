from fastapi import APIRouter

from app.core.dependencies import DBDep
from app.core.dependencies import admin_only
from app.services.aircrafts import AircraftsService
from app.schemas.aircrafts import AircraftResponse

router = APIRouter(
    prefix="/aircrafts",
    tags=["Самолеты"]
)

@router.post("", response_model=AircraftResponse, summary='Создать новый самолет')
async def create_aircraft(

):
    pass