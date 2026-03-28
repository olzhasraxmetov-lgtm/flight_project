from sqlalchemy import select

from app.mappers.seat_instances_map import SeatInstancesMapMapper
from app.repositories.base import BaseRepository
from app.models.seat_instances_map import SeatInstancesMapORM

class SeatInstancesMapRepository(BaseRepository):
    model = SeatInstancesMapORM
    mapper = SeatInstancesMapMapper

    async def get_ordered_seats_map(self, flight_instance_id: int):
        query = (
            select(self.model)
            .where(self.model.flight_instance_id == flight_instance_id)
            .order_by(self.model.row_number,
                      self.model.seat_letter)
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]