from app.mappers.base import DataMapper
from app.models.flights import FlightsORM
from app.schemas.flights import FlightResponse


class FlightMapper(DataMapper):
    db_model = FlightsORM
    schema = FlightResponse