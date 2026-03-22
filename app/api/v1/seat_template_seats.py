from fastapi import APIRouter

from app.core.dependencies import DBDep
from app.core.dependencies import admin_only
from app.schemas.seat_template_seats import SeatTemplateSeatCreate
from app.services.seat_template_seats import SeatTemplateSeatsService
router = APIRouter(
    prefix="/seat_template_seats",
    tags=["Места в шаблоне"]
)

@router.post("", summary='Создать места в шаблоне', dependencies=[admin_only])
async def create_aircraft(
    db: DBDep,
    payload: SeatTemplateSeatCreate
):
    return await SeatTemplateSeatsService(db).seat_template_seat_create(payload)