from app.mappers.base import DataMapper
from app.models.aircrafts import AircraftsORM
from app.schemas.aircrafts import AircraftResponse

class AircraftMapper(DataMapper):
    db_model = AircraftsORM
    schema = AircraftResponse