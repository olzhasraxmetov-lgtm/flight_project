from app.exceptions.base import ObjectNotFoundException, AirlineNotFoundException
from app.services.base import BaseService
from app.schemas.airlines import AirlineCreate, AirlineResponse, AirlineUpdate
from typing import Sequence, cast
from loguru import logger

class AirlinesService(BaseService):
    async def create_airline(self, payload: AirlineCreate):
        new_airline = await self.db.airlines.add(payload)
        await self.db.commit()
        return new_airline

    async def get_filtered_airlines_with_pagination(
            self,
            pagination,
            name: str | None
    ) -> Sequence[AirlineResponse]:
        result =  await self.db.airlines.get_paginated_items(
            limit=pagination.per_page or 5,
            offset=(pagination.page - 1) * (pagination.per_page or 5),
            name__ilike=name
        )
        return cast(Sequence[AirlineResponse], result)

    async def get_airline(self, airline_id: int) -> AirlineResponse:
        return await self.check_if_entity_exists(self.db.airlines, airline_id, AirlineNotFoundException)

    async def _edit_airline(self, airline_id: int, payload: AirlineUpdate, exclude_unset):
        try:
            updated_airline = await self.db.airlines.edit(data=payload, exclude_unset=exclude_unset, id=airline_id)
            await self.db.commit()
            logger.info(f"Airline updated successfully", airline_id=airline_id, updated_data=payload.model_dump(exclude_unset=True))
            return updated_airline
        except ObjectNotFoundException as ex:
            logger.warning("Failed to update airline: Not Found", airline_id=airline_id)
            raise AirlineNotFoundException from ex

    async def update_airline(self, airline_id: int, payload: AirlineUpdate):
        return await self._edit_airline(airline_id, payload, exclude_unset=False)

    async def partially_update_airline(self, airline_id: int, payload: AirlineUpdate):
        return await self._edit_airline(airline_id, payload, exclude_unset=True)

    async def delete_airline(self, airline_id: int):
        try:
            await self.db.airlines.delete(id=airline_id)
            await self.db.commit()
            logger.info(f"Airline deleted successfully", airline_id=airline_id)
        except ObjectNotFoundException as ex:
            logger.warning("Failed to delete airline: Not Found", airline_id=airline_id)
            raise AirlineNotFoundException from ex