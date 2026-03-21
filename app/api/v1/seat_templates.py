from fastapi import APIRouter

from app.core.dependencies import DBDep
from app.core.dependencies import admin_only
from app.schemas.seat_templates import SeatTemplateCreate, SeatTemplateResponse
from app.services.seat_templates import SeatTemplatesService

router = APIRouter(
    prefix="/seat_templates",
    tags=["Шаблоны мест"]
)

@router.post("", response_model=SeatTemplateResponse, summary='Создать новый шаблон для самолета', dependencies=[admin_only])
async def create_aircraft(
    db: DBDep,
    payload: SeatTemplateCreate,
):
    return await SeatTemplatesService(db).create_seat_template(payload)

@router.get("", response_model=list[SeatTemplateResponse], summary='Получить все шаблоны', dependencies=[admin_only])
async def get_all_aircrafts(
    db: DBDep,
):
    return await SeatTemplatesService(db).get_all_seat_templates()

@router.get("{seat_template_id}", response_model=SeatTemplateResponse, summary='Получить шаблон самолета по ID', dependencies=[admin_only])
async def get_aircraft_by_id(
    db: DBDep,
    seat_template_id: int
):
    return await SeatTemplatesService(db).get_seat_template_by_id(seat_template_id)