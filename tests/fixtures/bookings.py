import pytest

from app.schemas.bookings import PassengerCreate, BookingCreateRequest
from app.services.bookings import BookingService

@pytest.fixture
def booking_service(db):
    return BookingService(db)

@pytest.fixture
async def created_booking(db, registered_user, created_flight_instance):
    booking_service = BookingService(db)
    all_seats = await db.seat_instances_map.get_all(flight_instance_id=created_flight_instance.id)
    seat_ids = [all_seats[0].id, all_seats[1].id]

    passengers = [
        PassengerCreate(
            first_name="Mikey",
            last_name="Doe",
            passport_number="Rc3lXHa",
            seat_instance_id=seat_ids[0],
        ),
        PassengerCreate(
            first_name="Wisley",
            last_name="Doe",
            passport_number="Tc1lXHb",
            seat_instance_id=seat_ids[1],
        )
    ]

    payload = BookingCreateRequest(
        flight_instance_id=created_flight_instance.id,
        passengers=passengers
    )

    return await booking_service.create_booking(user_id=registered_user.id, payload=payload)
