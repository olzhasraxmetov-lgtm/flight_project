from app.mappers.seat_template_seats import SeatTemplateSeatsMapper
from app.repositories.base import BaseRepository
from app.models.seat_template_seat import SeatTemplateSeatsORM

class SeatTemplateSeatsRepository(BaseRepository):
    model = SeatTemplateSeatsORM
    mapper = SeatTemplateSeatsMapper