from fastapi import APIRouter

from app.core.dependencies import DBDep
from app.core.dependencies import admin_only
from app.services.seat_templates import SeatTemplatesService

router = APIRouter(
    prefix="/seat_templates",
    tags=["Шаблоны мест"]
)

@router.post("", summary='Создать новый шаблон для самолета', dependencies=[admin_only])
async def create_aircraft(
    db: DBDep,
):
    pass