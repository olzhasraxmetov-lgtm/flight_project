from decimal import Decimal
from typing import Any
from uuid import uuid4

from anyio import to_thread
from loguru import logger
from sqlalchemy.exc import SQLAlchemyError
from app.tasks.emails import send_email_after_payment
from app.core.dependencies import DBDep
from app.exceptions.base import BookingAlreadyPaidException, ForbiddenBookingException, ObjectNotFoundException, \
    BookingNotFoundException, PaymentNotFoundException
from app.helpers.booking_status import BookingStatus
from app.services.base import BaseService
from yookassa import Configuration, Payment
from yookassa.domain.notification import WebhookNotificationFactory
from app.helpers.payment_status import PaymentStatus

class PaymentsService(BaseService):
    def __init__(self, db: DBDep, shop_id: str, secret_key: str):
        super().__init__(db)

        self.shop_id = shop_id
        self.secret_key = secret_key

        Configuration.account_id = self.shop_id
        Configuration.secret_key = self.secret_key

    async def create_yookassa_payment(self,*,booking_id: int, amount: Decimal, user_email: str, description: str,) -> dict[str, Any]:
        if not self.shop_id or not self.secret_key:
            raise RuntimeError("Задайте YOOKASSA_SHOP_ID и YOOKASSA_SECRET_KEY в .env")
        payload = {
            "amount": {
                "value": f"{amount:.2f}",
                "currency": "RUB",
            },
            "confirmation": {
                "type": "redirect",
                "return_url": f'https://learnedly-unportioned-courtney.ngrok-free.dev/payments/success?payment_id={booking_id}',
            },
            "capture": True,
            "description": description,
            "metadata": {
                "booking_id": booking_id,
            },
            "receipt": {
                "customer": {
                    "email": user_email,
                },
                "items": [
                    {
                        "description": description[:128],
                        "quantity": "1.00",
                        "amount": {
                            "value": f"{amount:.2f}",
                            "currency": "RUB",
                        },
                        "vat_code": 1,
                        "payment_mode": "full_prepayment",
                        "payment_subject": "commodity",
                    },
                ],
            },
        }

        def _request() -> Any:
            return Payment.create(payload, str(uuid4()))

        payment = await to_thread.run_sync(_request)

        confirmation_url = getattr(payment.confirmation, "confirmation_url", None)
        logger.info(
            "YooKassa payment created",
            payment_id=payment.id,
            booking_id=booking_id,
            status=payment.status
        )
        return {
            "id": payment.id,
            "status": payment.status,
            "confirmation_url": confirmation_url,
        }

    async def initiate_payment(self, booking_id: int, user_email: str, user_id: int) -> dict[str, Any]:
        try:
            booking = await self.db.bookings.get_booking_with_passengers(booking_id=booking_id)
        except ObjectNotFoundException:
            raise BookingNotFoundException

        if booking.user_id != user_id:
            raise ForbiddenBookingException

        if booking.status == BookingStatus.CONFIRMED:
            raise BookingAlreadyPaidException

        payment_data = await self.create_yookassa_payment(
            booking_id=booking.id,
            amount=booking.total_price,
            user_email=user_email,
            description=f"Оплата бронирования {booking.booking_reference}"
        )

        new_payment = await self.db.payments.add({
            "booking_id": booking_id,
            "transaction_id": payment_data["id"],
            "amount": booking.total_price,
            "status": PaymentStatus.PENDING,
            "payment_method": "yookassa"
        })

        await self.db.commit()
        logger.info(
            "Payment initiated and saved to DB",
            booking_id=booking_id,
            transaction_id=new_payment.id
        )
        return {"url": payment_data["confirmation_url"]}

    async def handle_webhook(self, booking_id: int, status: str):
        logger.info("Processing webhook", booking_id=booking_id, status=status)
        try:
            payment = await self.db.payments.get_one(booking_id=booking_id)
        except ObjectNotFoundException:
            raise PaymentNotFoundException

        status_str = str(status.value if hasattr(status, 'value') else status)

        try:
            if status_str == "succeeded":
                await self.db.payments.edit(
                    data={"status": PaymentStatus.SUCCEEDED},
                    booking_id=booking_id,
                )
                try:
                    booking = await self.db.bookings.get_booking_with_passengers(booking_id=payment.booking_id)
                    booking.status = BookingStatus.CONFIRMED
                    send_email_after_payment.delay(payment.booking_id)
                    logger.info(
                        "Payment and booking confirmed via webhook",
                        booking_id=payment.booking_id
                    )
                except ObjectNotFoundException:
                    logger.error(
                        f"Integrity error: Payment {payment.id} exists for non-existing booking {payment.booking_id}")

            elif status_str in ["canceled", "failed"]:
                await self.db.payments.edit(
                    data={"status": PaymentStatus.FAILED},
                    id=payment.id,
                )
                logger.warning(
                    "Payment failed via webhook",
                    booking_id=booking_id,
                    status=status_str
                )
            await self.db.commit()

        except SQLAlchemyError as e:
            await self.db.session.rollback()
            logger.error(f"Database error during booking confirmation: {e}")
            raise

    async def webhook_logic(self, event_data: dict):
        """Парсинг уведомления и маршрутизация логики."""
        try:
            notification_object = WebhookNotificationFactory().create(event_data)
            payment_object = notification_object.object

            booking_id = payment_object.metadata.get("booking_id")
        except Exception as e:
            logger.error(f"Webhook parsing error: {e}")
            return {"status": "error", "message": "Invalid data"}

        await self.handle_webhook(
            status=payment_object.status,
            booking_id = int(booking_id) if booking_id else None
        )
        logger.info("Webhook handled successfully", transaction_id=payment_object.id)
        return {"status": "ok"}


    async def handle_payment_status(self, payment_id: int):
        purchase = await self.db.payments.get_one(id=payment_id)

        if not purchase:
            return {
                "status": "error",
                "message": "Покупка не найдена. Если вы уверены, что оплатили, обратитесь в поддержку."
            }
        if purchase.status == PaymentStatus.SUCCEEDED:
            return {
                "status": "success",
                "message": f"Заказ '{purchase.transaction_id}' успешно оплачен!",
                "payment_id": purchase.id
            }
        return {
            "status": "pending",
            "message": "Платеж обрабатывается. Обновите страницу через несколько секунд.",
            "payment_id": purchase.id
        }