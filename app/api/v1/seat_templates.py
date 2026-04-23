from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.core.dependencies import DBDep
from app.core.dependencies import admin_only
from app.schemas.seat_templates import SeatTemplateCreate, SeatTemplateResponse, SeatTemplateUpdate
from app.services.seat_templates import SeatTemplatesService

router = APIRouter(
    prefix="/seat_templates",
    tags=["Шаблоны мест"]
)

@router.post("", response_model=SeatTemplateResponse, summary='Создать новый шаблон для самолета', dependencies=[admin_only])
async def create_seat_template(
    db: DBDep,
    payload: SeatTemplateCreate,
):
    return await SeatTemplatesService(db).create_seat_template(payload)

@router.get(
    "",
    response_model=list[SeatTemplateResponse],
    summary='Получить все шаблоны',
    dependencies=[admin_only]
)
@cache(expire=60)
async def get_all_seat_templates(
    db: DBDep,
):
    return await SeatTemplatesService(db).get_all_seat_templates()

@router.get(
    "/{seat_template_id}",
    response_model=SeatTemplateResponse,
    summary='Получить шаблон самолета по ID',
    dependencies=[admin_only]
)
@cache(expire=30)
async def get_seat_template_by_id(
    db: DBDep,
    seat_template_id: int
):
    return await SeatTemplatesService(db).get_seat_template_by_id(seat_template_id)

@router.put(
    "/{seat_template_id}",
    response_model=SeatTemplateResponse,
    summary='Обновить шаблон самолета по ID',
    dependencies=[admin_only]
)
async def update_seat_template(
    db: DBDep,
    payload: SeatTemplateUpdate,
    seat_template_id: int
):
    return await SeatTemplatesService(db).update_seat_template(seat_template_id, payload)

@router.patch(
    "/{seat_template_id}",
    response_model=SeatTemplateResponse,
    summary='Частично обновить шаблон самолета по ID',
    dependencies=[admin_only]
)
async def partially_update_seat_template(
    db: DBDep,
    payload: SeatTemplateUpdate,
    seat_template_id: int
):
    return await SeatTemplatesService(db).partially_update_seat_template(seat_template_id, payload)

@router.delete(
    "/{seat_template_id}",
    summary='Удалить шаблон самолета по ID',
    dependencies=[admin_only],
    status_code=204,
)
async def delete_seat_template(
    db: DBDep,
    seat_template_id: int
):
    return await SeatTemplatesService(db).delete_seat_template(seat_template_id)