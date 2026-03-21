from app.mappers.base import DataMapper
from app.models.seat_templates import SeamTemplatesORM
from app.schemas.seat_templates import SeatTemplateResponse

class SeatTemplateMapper(DataMapper):
    db_model = SeamTemplatesORM
    schema = SeatTemplateResponse