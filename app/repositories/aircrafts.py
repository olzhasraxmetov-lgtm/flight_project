from app.mappers.aircrafts import AircraftMapper
from app.repositories.base import BaseRepository
from app.models.aircrafts import AircraftsORM

class AircraftsRepository(BaseRepository):
    model = AircraftsORM
    mapper = AircraftMapper