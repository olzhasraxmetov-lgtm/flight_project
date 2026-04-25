from sqlalchemy import select, update

from app.mappers.seat_instances_map import SeatInstancesMapMapper
from app.repositories.base import BaseRepository
from app.models.seat_instances_map import SeatInstancesMapORM
from app.helpers.seat_status import SeatStatus

class SeatInstancesMapRepository(BaseRepository):
    model = SeatInstancesMapORM
    mapper = SeatInstancesMapMapper

    async def validate_seats_for_flight(self, flight_instance_id: int, seat_ids: list[int]):
        query = select(
            self.model
        ).where(
            self.model.id.in_(seat_ids),
            self.model.flight_instance_id == flight_instance_id,
            self.model.status == SeatStatus.AVAILABLE
        )
        res = await self.session.execute(query)
        found_seats = res.scalars().all()

        return found_seats

    async def update_status(self, seat_ids: list[int], seat_status: SeatStatus):
        if not seat_ids:
            return
        query = (
            update(self.model)
            .where(self.model.id.in_(seat_ids))
            .values(status=seat_status)
        )
        await self.session.execute(query)


    async def get_ordered_seats_map(self, flight_instance_id: int, map_res: bool = True):
        query = (
            select(self.model)
            .where(self.model.flight_instance_id == flight_instance_id)
            .order_by(self.model.row_number,
                      self.model.seat_letter)
        )
        result = await self.session.execute(query)
        return [self._map(model, map_res) for model in result.scalars().all()]