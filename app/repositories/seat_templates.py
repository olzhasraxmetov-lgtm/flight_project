from app.mappers.seat_templates import SeatTemplateMapper
from app.repositories.base import BaseRepository
from app.models.seat_templates import SeamTemplatesORM

class SeatTemplatesRepository(BaseRepository):
    model = SeamTemplatesORM
    mapper = SeatTemplateMapper