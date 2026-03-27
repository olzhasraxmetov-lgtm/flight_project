from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.exceptions.base import ObjectNotFoundException
from app.mappers.flight_instances import FlightInstancesMapper
from app.models.flight_instances import FlightInstancesORM
from app.repositories.base import BaseRepository



class FlightInstancesRepository(BaseRepository):
    model = FlightInstancesORM
    mapper = FlightInstancesMapper

    async def get_one_with_details(self, flight_instance_id: int):
        query = (
            select(self.model)
            .where(self.model.id == flight_instance_id)
            .options(
                joinedload(self.model.arrival_airport),
                joinedload(self.model.departure_airport),
            )
        )
        result = await self.session.execute(query)
        model = result.unique().scalar_one_or_none()
        if not model:
            raise ObjectNotFoundException()
        return self.mapper.map_to_domain_entity(model)