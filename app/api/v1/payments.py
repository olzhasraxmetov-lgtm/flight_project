from fastapi import APIRouter, Request, Query

from app.core.dependencies import DBDep, CurrentUser
from app.services.payments import PaymentsService
from app.core.config import settings
router = APIRouter(
    prefix="/payments",
    tags=["Оплата"],
)

@router.post('', summary='Оплатить бронь')
async def pay_booking(
    db: DBDep,
    booking_id: int,
    user: CurrentUser
):
    return await PaymentsService(
        db,
        shop_id=settings.YOOKASSA_SHOP_ID,
        secret_key=settings.YOOKASSA_API_SECRET_KEY
    ).initiate_payment(booking_id=booking_id, user_email=user.email, user_id=user.id)

@router.get('/success', summary='После успешной оплаты курса перенаправляет на этот эндпоинт')
async def payment_success_page(
        db: DBDep,
        payment_id: int = Query(...),
):
    return await PaymentsService(
        db,
        shop_id=settings.YOOKASSA_SHOP_ID,
        secret_key=settings.YOOKASSA_API_SECRET_KEY
    ).handle_payment_status(payment_id)

@router.post('/webhook',
                      summary="Обработка уведомлений от ЮKassa",
                      description="Принимает POST-запросы от платежной системы при изменении статуса платежа"
                      )
async def yookassa_webhook(
    db: DBDep,
    request: Request,
):
    data = await  request.json()
    return await PaymentsService(
        db,
        shop_id=settings.YOOKASSA_SHOP_ID,
        secret_key=settings.YOOKASSA_API_SECRET_KEY
    ).webhook_logic(data)