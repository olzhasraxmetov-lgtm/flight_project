from app.mappers.base import DataMapper
from app.models.flight_instances import FlightInstancesORM
from app.schemas.flight_instances import FlightInstanceResponse


class FlightInstancesMapper(DataMapper):
    db_model = FlightInstancesORM
    schema = FlightInstanceResponse