from app.mappers.flight_instances import FlightInstancesMapper
from app.models.flight_instances import FlightInstancesORM
from app.repositories.base import BaseRepository



class FlightInstancesRepository(BaseRepository):
    model = FlightInstancesORM
    mapper = FlightInstancesMapper
