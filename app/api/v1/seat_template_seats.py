from fastapi import APIRouter

from app.core.dependencies import DBDep
from app.core.dependencies import admin_only
from app.schemas.seat_template_seats import SeatTemplateSeatCreate, SeatTemplateMapResponse
from app.schemas.seat_template_seats import SeatGenerationResponse
from app.services.seat_template_seats import SeatTemplateSeatsService
router = APIRouter(
    prefix="/seat_template_seats",
    tags=["Места в шаблоне"]
)

@router.post(
    "",
    summary='Создать места в шаблоне',
    dependencies=[admin_only],
    response_model=SeatGenerationResponse
)
async def create_seat_template_seats(
    db: DBDep,
    payload: SeatTemplateSeatCreate
):
    return await SeatTemplateSeatsService(db).seat_template_seat_create(payload)

@router.get(
    "/{template_id}/seats",
    summary='Получить места для шаблона',
    response_model=SeatTemplateMapResponse,
    dependencies=[admin_only],
)
async def get_seat_template_seats(db: DBDep, template_id: int):
    return await SeatTemplateSeatsService(db).get_seat_template_seats(template_id)

@router.delete(
    "/{template_id}",
    summary='Удалить места для шаблона',
    status_code=204,
    dependencies=[admin_only],
)
async def delete_seat_template_seats(db: DBDep, template_id: int):
    return await SeatTemplateSeatsService(db).delete_seat_template_seats(template_id)