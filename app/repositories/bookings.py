from datetime import datetime, timezone, timedelta

from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.exceptions.base import BookingNotFoundException, ObjectNotFoundException
from app.helpers.booking_status import BookingStatus
from app.mappers.bookings import BookingMapper
from app.repositories.base import BaseRepository
from app.models.bookings import BookingsORM
from app.models.passengers import PassengersORM

class BookingsRepository(BaseRepository):
    model = BookingsORM
    mapper = BookingMapper

    async def get_booking_with_passengers(self, booking_id: int):
        query = (
            select(self.model)
            .where(self.model.id == booking_id)
            .options(
                selectinload(self.model.passengers),
                selectinload(self.model.passengers).joinedload(PassengersORM.flight_instance)
            )
        )
        result = await self.session.execute(query)
        full_booking = result.unique().scalar_one_or_none()
        if not full_booking:
            raise ObjectNotFoundException
        return full_booking

    async def get_expired_bookings(self, minutes: int = 1):
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        threshold = now - timedelta(minutes=minutes)
        stmt = (
            select(self.model)
            .where(self.model.status == BookingStatus.CREATED,
                   self.model.created_at <= threshold)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_user_bookings(self, user_id: int):
        query = (
            select(self.model)
            .where(self.model.user_id == user_id)
            .options(
                selectinload(self.model.passengers),
                selectinload(self.model.passengers).joinedload(PassengersORM.flight_instance)
            )
        )
        result = await self.session.execute(query)
        bookings = result.unique().scalars().all()
        return bookings