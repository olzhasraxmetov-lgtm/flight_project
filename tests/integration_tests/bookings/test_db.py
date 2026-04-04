import pytest

from app.exceptions.base import BookingNotFoundException, ForbiddenBookingException, PassengerNotFoundException, \
    SeatsNotAvailableException
from app.helpers.booking_status import BookingStatus
from app.helpers.seat_status import SeatStatus
from app.schemas.bookings import BookingCreateRequest, PassengerCreate


async def test_create_booking(db, registered_user, created_booking):
    assert created_booking.booking_reference is not None
    assert created_booking.status == BookingStatus.CREATED
    assert created_booking.user_id == registered_user.id
    assert len(created_booking.passengers) == 2


async def test_get_booking_by_id(booking_service, registered_user, created_booking):
    booking = await booking_service.get_booking(created_booking.id)
    assert booking is not None
    assert booking.booking_reference == created_booking.booking_reference
    assert booking.id == created_booking.id

async def test_get_my_bookings(booking_service, registered_user, created_booking):
    bookings = await booking_service.get_my_bookings(registered_user.id)
    assert isinstance(bookings, list)
    assert len(bookings) == 1

async def test_delete_booking_fully(booking_service, registered_user, created_booking):
    result = await booking_service.delete_booking_fully(created_booking.id)
    assert result['detail'] == "Бронирование успешно удалено"

    with pytest.raises(BookingNotFoundException):
        await booking_service.get_booking(created_booking.id)

async def test_delete_passenger_in_booking(booking_service, registered_user, created_booking):
    old_total_price = created_booking.total_price
    passenger_id = created_booking.passengers[0].id
    result = await booking_service.delete_passenger_in_booking(
        passenger_id=passenger_id,
        booking_id=created_booking.id,
        user_id=registered_user.id
    )
    assert isinstance(result, dict)
    assert result["status"] == "success"
    assert old_total_price != result["new_total_price"]
    assert result["message"] == f"Passenger {passenger_id} removed"

async def test_forbidden_delete_passenger(booking_service, simple_user_forbidden, created_booking):
    passenger_id = created_booking.passengers[0].id
    with pytest.raises(ForbiddenBookingException):
        await booking_service.delete_passenger_in_booking(
            passenger_id=passenger_id,
            booking_id=created_booking.id,
            user_id=simple_user_forbidden.id
        )

async def test_passenger_not_found(booking_service, registered_user, created_booking):
    with pytest.raises(PassengerNotFoundException):
        await booking_service.delete_passenger_in_booking(
            passenger_id=123123,
            booking_id=created_booking.id,
            user_id=registered_user.id
        )


async def test_create_booking_atomic_rollback(booking_service, db, registered_user, created_flight_instance):
    all_seats = await db.seat_instances_map.get_all(flight_instance_id=created_flight_instance.id)
    await db.seat_instances_map.update_status([all_seats[0].id], seat_status=SeatStatus.RESERVED)
    await db.session.commit()

    passengers = [
        PassengerCreate(
            first_name="Diana",
            last_name="someone",
            passport_number="Rc3lXHa",
            seat_instance_id=all_seats[0].id
        ),
        PassengerCreate(
            first_name="Someone",
            last_name="someone",
            passport_number="Tc1lXHb",
            seat_instance_id=all_seats[1].id
        )
    ]

    payload = BookingCreateRequest(
        flight_instance_id=created_flight_instance.id,
        passengers=passengers
    )
    with pytest.raises(SeatsNotAvailableException):
        await booking_service.create_booking(user_id=registered_user.id, payload=payload)

    user_bookings = await db.bookings.get_user_bookings(registered_user.id)
    assert len(user_bookings) == 0