from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.exceptions.base import ObjectNotFoundException
from app.mappers.flights import FlightMapper
from app.models.flights import FlightsORM
from app.repositories.base import BaseRepository



class FlightsRepository(BaseRepository):
    model = FlightsORM
    mapper = FlightMapper


    async def get_flight_with_rels(self, flight_id: int):
        query = (
            select(FlightsORM)
            .where(FlightsORM.id == flight_id)
            .options(
                joinedload(FlightsORM.departure_airport),
                joinedload(FlightsORM.arrival_airport),
                joinedload(FlightsORM.airline),
            )
        )
        result = await self.session.execute(query)

        model = result.unique().scalar_one_or_none()
        if not model:
            raise ObjectNotFoundException()
        return self.mapper.map_to_domain_entity(model)
