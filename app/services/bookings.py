from decimal import Decimal

from app.exceptions.base import FlightNotAvailableForBookingException, SeatsNotAvailableException
from app.helpers.booking_status import BookingStatus
from app.helpers.flight_status import FlightStatus
from app.schemas.bookings import BookingCreateRequest, BookingInternalCreate, \
    PassengerInternalCreateRequest, MyBookingsResponse
from app.services.base import BaseService
from app.services.flight_instances import FlightInstancesService

from app.utils.pnr_generator import generate_pnr_identifier

class BookingService(BaseService):


    async def create_booking(
        self,
        user_id: int,
        payload: BookingCreateRequest,
    ):
        flight_service = FlightInstancesService(self.db)
        flight = await flight_service.validate_flight_for_booking(payload.flight_instance_id)

        if flight.status != FlightStatus.SCHEDULED:
            raise FlightNotAvailableForBookingException

        seat_ids = [passenger.seat_instance_id for passenger in payload.passengers]

        found_seats = await self.db.seat_instances_map.validate_seats_for_flight(payload.flight_instance_id, seat_ids)

        if len(found_seats) != len(seat_ids):
            raise SeatsNotAvailableException

        booking_pnr = generate_pnr_identifier()
        total_price = Decimal(flight.base_price * len(seat_ids))
        booking_data = BookingInternalCreate(
            user_id=user_id,
            booking_reference=booking_pnr,
            total_price=total_price,
            status=BookingStatus.CREATED,
        )
        new_booking = await self.db.bookings.add(booking_data, map_res=False)

        await self.db.session.flush()

        passengers = [
            PassengerInternalCreateRequest(
                **p.model_dump(),
                booking_id=new_booking.id,
                flight_instance_id=flight.id,
                price=flight.base_price
            )

            for p in payload.passengers
        ]

        await self.db.passengers.add_bulk(passengers)
        await self.db.seat_instances_map.mark_as_booked(seat_ids)
        await self.db.commit()

        return await self.db.bookings.get_booking_with_passengers(booking_id=new_booking.id)

    async def get_my_bookings(self, user_id: int) -> list[MyBookingsResponse]:
        bookings_orm = await self.db.bookings.get_user_bookings(user_id)

        result = []
        for b in bookings_orm:
            first_p = b.passengers[0] if b.passengers else None
            f_inst = first_p.flight_instance if first_p else None

            result.append(MyBookingsResponse(
                id=b.id,
                booking_reference=b.booking_reference,
                total_price=b.total_price,
                status=b.status,
                created_at=b.created_at,
                flight_number=f_inst.flight_number if f_inst else None,
                departure_at=f_inst.departure_at if f_inst else None,
                arrival_at=f_inst.arrival_at if f_inst else None,
                passengers_count=len(b.passengers)
            ))
        return result