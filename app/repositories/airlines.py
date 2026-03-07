from app.mappers.airlines import AirlinesMapper
from app.repositories.base import BaseRepository
from app.models.airlines import AirlinesORM

class AirlinesRepository(BaseRepository):
    model = AirlinesORM
    mapper = AirlinesMapper