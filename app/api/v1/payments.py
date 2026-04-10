from fastapi import APIRouter

from app.core.dependencies import DBDep
from app.services.payments import PaymentsService

router = APIRouter(
    prefix="/payments",
    tags=["Оплата"],
)

@router.post('', summary='Оплатить бронь')
async def pay_booking(
    db: DBDep,
):
    return await PaymentsService(db).create_payment()