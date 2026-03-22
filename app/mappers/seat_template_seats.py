from app.mappers.base import DataMapper
from app.models.seat_template_seat import SeatTemplateSeatsORM
from app.schemas.seat_template_seats import SeatTemplateSeatResponse

class SeatTemplateSeatsMapper(DataMapper):
    db_model = SeatTemplateSeatsORM
    schema = SeatTemplateSeatResponse
