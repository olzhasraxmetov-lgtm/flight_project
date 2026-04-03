from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload

from app.mappers.bookings import BookingMapper
from app.repositories.base import BaseRepository
from app.models.bookings import BookingsORM
from app.models.flight_instances import FlightInstancesORM
from app.models.passengers import PassengersORM

class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingMapper

    async def get_booking_with_passengers(self, booking_id: int):
        query = (
            select(self.model)
            .where(self.model.id == booking_id)
            .options(
                selectinload(self.model.passengers)
                .joinedload(PassengersORM.flight_instance)
            )
        )
        result = await self.session.execute(query)
        full_booking = result.unique().scalar_one()
        return full_booking