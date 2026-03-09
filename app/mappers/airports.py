from app.mappers.base import DataMapper
from app.models.airports import AirportsORM
from app.schemas.airports import AirportResponse


class AirportMapper(DataMapper):
    db_model = AirportsORM
    schema = AirportResponse