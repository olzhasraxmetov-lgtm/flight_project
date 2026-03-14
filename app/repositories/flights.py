from app.mappers.flights import FlightMapper
from app.models.flights import FlightsORM
from app.repositories.base import BaseRepository



class FlightsRepository(BaseRepository):
    db_model = FlightsORM
    mapper = FlightMapper