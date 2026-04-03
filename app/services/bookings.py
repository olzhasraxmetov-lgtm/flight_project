from decimal import Decimal

from app.exceptions.base import FlightNotAvailableForBookingException, SeatsNotAvailableException, \
    BookingNotFoundException, ObjectNotFoundException, PassengerNotFoundException
from app.helpers.booking_status import BookingStatus
from app.helpers.flight_status import FlightStatus
from app.helpers.seat_status import SeatStatus
from app.schemas.bookings import BookingCreateRequest, BookingInternalCreate, \
    PassengerInternalCreateRequest, MyBookingsResponse
from app.services.base import BaseService
from app.services.flight_instances import FlightInstancesService

from app.utils.pnr_generator import generate_pnr_identifier

class BookingService(BaseService):

    async def get_booking_or_404(self, booking_id: int):
        try:
            return await self.db.bookings.get_booking_with_passengers(booking_id)
        except ObjectNotFoundException:
            raise BookingNotFoundException

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
        await self.db.seat_instances_map.update_status(seat_ids, seat_status=SeatStatus.RESERVED)
        await self.db.commit()

        return await self.db.bookings.get_booking_with_passengers(booking_id=new_booking.id)

    async def get_my_bookings(self, user_id: int) -> list[MyBookingsResponse]:
        return await self.db.bookings.get_user_bookings(user_id)

    async def get_booking(self, booking_id: int):
         return await self.get_booking_or_404(booking_id)

    async def delete_booking_fully(self, booking_id: int):
        booking = await self.get_booking_or_404(booking_id)
        seat_ids = [p.seat_instance_id for p in booking.passengers]
        if seat_ids:
         await self.db.seat_instances_map.update_status(seat_ids, seat_status=SeatStatus.AVAILABLE)

        await self.db.bookings.delete(id=booking_id)
        await self.db.commit()
        return {"detail": "Бронирование успешно удалено"}

    async def delete_passenger_in_booking(self, passenger_id: int, booking_id: int):
        booking = await self.get_booking_or_404(booking_id)
        if len(booking.passengers) == 1:
            return await self.delete_booking_fully(booking_id)
        passenger = next((p for p in booking.passengers if p.id == passenger_id), None)
        if not passenger:
            raise PassengerNotFoundException

        await self.db.seat_instances_map.update_status([passenger.seat_instance_id], seat_status=SeatStatus.AVAILABLE)
        booking.total_price -= passenger.price
        booking.passengers.remove(passenger)

        await self.db.session.flush()
        await self.db.commit()
        return {
            "status": "success",
            "message": f"Passenger {passenger_id} removed",
            "new_total_price": booking.total_price
        }

