from app.mappers.base import DataMapper
from app.models.bookings import BookingsORM
from app.schemas.bookings import BookingFullResponse


class BookingMapper(DataMapper):
    db_model = BookingsORM
    schema = BookingFullResponse