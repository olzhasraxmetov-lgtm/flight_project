from app.mappers.seat_instances_map import SeatInstancesMapMapper
from app.repositories.base import BaseRepository
from app.models.seat_instances_map import SeatInstancesMapORM

class SeatInstancesMapRepository(BaseRepository):
    model = SeatInstancesMapORM
    mapper = SeatInstancesMapMapper