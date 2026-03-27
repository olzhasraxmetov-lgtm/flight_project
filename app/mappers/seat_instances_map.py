from app.mappers.base import DataMapper
from app.models.seat_instances_map import SeatInstancesMapORM
from app.schemas.seat_instanes_map import SeatInstanceMapResponse

class SeatInstancesMapMapper(DataMapper):
    db_model = SeatInstancesMapORM
    schema = SeatInstanceMapResponse
