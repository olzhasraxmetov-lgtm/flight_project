from app.helpers.booking_status import BookingStatus
from app.repositories.payments import PaymentsRepository
from app.helpers.payment_status import PaymentStatus
from unittest.mock import patch


async def test_create_payment(auth_user, created_booking, db):
    response = await auth_user.post(f'/payments/{created_booking.id}')
    data = response.json()
    assert response.status_code == 200
    assert 'url' in data
    assert isinstance(data['url'], str)

    repo = PaymentsRepository(db.session)

    payment = await repo.get_one_or_none(booking_id=created_booking.id)
    assert payment is not None
    assert payment.status == PaymentStatus.PENDING

async def test_create_payment_twice(auth_user, created_booking, db):
    response1 = await auth_user.post(f'/payments/{created_booking.id}')
    assert response1.status_code == 200

    response2 = await auth_user.post(f'/payments/{created_booking.id}')
    assert response2.status_code == 200

    repo = PaymentsRepository(db.session)
    payments = await repo.get_all(booking_id=created_booking.id)
    assert len(payments) == 2

async def test_create_payment_not_found(auth_user, db):
    response = await auth_user.post('/payments/999999')
    assert response.status_code == 404
    assert response.json()["detail"] == "Бронирование не найдено"


async def test_create_payment_already_paid(auth_user, created_booking, db):
    from app.models.bookings import BookingStatus
    created_booking.status = BookingStatus.CONFIRMED
    await db.session.commit()

    response = await auth_user.post(f'/payments/{created_booking.id}')

    assert response.status_code == 409
    assert response.json()["detail"] == "Ваш заказ уже оплачен"


async def test_yookassa_webhook_success(ac, db, created_booking,create_payment, mock_email_task):
    tx_id = "success_123"
    await create_payment(created_booking.id, created_booking.total_price, transaction_id=tx_id)

    yookassa_payload = {
        "type": "notification",
        "event": "payment.succeeded",
        "object": {
            "id": tx_id,
            "status": "succeeded",
            "metadata": {
                "booking_id": str(created_booking.id)
            }
        }
    }

    response = await ac.post("/webhooks/yookassa", json=yookassa_payload)
    assert response.status_code == 200

    mock_email_task.assert_called_once()
    mock_email_task.assert_called_with(created_booking.id)

    await db.session.refresh(created_booking)
    assert created_booking.status == BookingStatus.CONFIRMED


async def test_yookassa_webhook_payment_failed(ac, db, created_booking,create_payment, mock_email_task):
    fake_transaction_id  = "fail_12345"
    await create_payment(created_booking.id, created_booking.total_price, transaction_id=fake_transaction_id)

    yookassa_payload = {
        "type": "notification",
        "event": "payment.canceled",
        "object": {
            "id": fake_transaction_id,
            "status": "canceled",
            "metadata": {"booking_id": str(created_booking.id)}
        }
    }

    response = await ac.post("/webhooks/yookassa", json=yookassa_payload)
    assert response.status_code == 200

    mock_email_task.assert_not_called()

    await db.session.refresh(created_booking)
    await db.session.refresh(created_booking)
    assert created_booking.status == BookingStatus.CREATED

async def test_yookassa_webhook_payment_handle_status(auth_user, db, created_booking, mock_email_task):
    response = await auth_user.post(f'/payments/{created_booking.id}')
    assert response.status_code == 200

    repo = PaymentsRepository(db.session)
    payment = await repo.get_one_or_none(booking_id=created_booking.id)
    assert payment is not None

    yookassa_payload = {
        "type": "notification",
        "event": "payment.succeeded",
        "object": {
            "id": payment.transaction_id,
            "status": "succeeded",
            "metadata": {"booking_id": str(created_booking.id)}
        }
    }

    response = await auth_user.post("/webhooks/yookassa", json=yookassa_payload)
    assert response.status_code == 200

    mock_email_task.assert_called_once()
    mock_email_task.assert_called_with(created_booking.id)


    response_get = await auth_user.get(f'/payments/success?payment_id={payment.id}')
    assert response_get.status_code == 200
    data = response_get.json()
    assert data["status"] == "success"
    assert data["message"] == f"Заказ '{payment.transaction_id}' успешно оплачен!"
    assert data["payment_id"] == payment.id