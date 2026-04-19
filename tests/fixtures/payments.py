import pytest


@pytest.fixture
async def create_payment(db):
    """Фабрика для быстрого создания платежа в БД."""
    async def _create(booking_id: int, price: float, transaction_id: str):
        from app.models.payments import PaymentStatus
        await db.payments.add({
            "booking_id": booking_id,
            "status": PaymentStatus.PENDING,
            "amount": price,
            "transaction_id": transaction_id,
            "payment_method": "yookassa",
        })
        await db.session.commit()
    return _create