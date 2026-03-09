from app.mappers.airports import AirportsORM
from app.repositories.base import BaseRepository
from app.mappers.airports import AirportMapper

class AirportsRepository(BaseRepository):
    model = AirportsORM
    mapper = AirportMapper