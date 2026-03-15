from typing import Sequence
from app.schemas.airports import AirportCreate, AirportResponse, AirportUpdate
from app.services.base import BaseService
from app.exceptions.base import ObjectNotFoundException, AirportNotFoundException
from loguru import logger

class AirportsService(BaseService):
    async def create_airport(self, payload: AirportCreate) -> AirportResponse:
        new_airport = await self.db.airports.add(payload)
        await self.db.commit()
        return new_airport

    async def get_filtered_airports_with_pagination(
            self,
            pagination,
            city: str | None,
            country: str | None,
            name: str | None
    ) -> Sequence[AirportResponse]:
        per_page = pagination.per_page or 5
        return await self.db.airports.get_paginated_items(
            limit=per_page,
            offset=per_page * (pagination.page - 1),
            city=city,
            country=country,
            name=name,
        )

    async def get_airport_by_id(self, airport_id: int) -> AirportResponse:
         return await self.check_if_entity_exists(self.db.airports, airport_id, AirportNotFoundException)

    async def _edit_airport(self, airport_id: int, payload: AirportUpdate, exclude_unset):
        try:
            updated_airport = await self.db.airports.edit(data=payload, exclude_unset=exclude_unset, id=airport_id)
            await self.db.commit()
            logger.info(f"Airport updated successfully", airport_id=airport_id, updated_data=payload.model_dump(exclude_unset=True))
            return updated_airport
        except ObjectNotFoundException as ex:
            logger.warning("Failed to update airport: Not Found", airport_id=airport_id)
            raise AirportNotFoundException from ex

    async def update_airline(self, airport_id: int, payload: AirportUpdate):
        return await self._edit_airport(airport_id, payload, exclude_unset=False)

    async def partially_update_airline(self, airport_id: int, payload: AirportUpdate):
        return await self._edit_airport(airport_id, payload, exclude_unset=True)

    async def delete_airport(self, airport_id: int):
        try:
            await self.db.airports.delete(id=airport_id)
            await self.db.commit()
            logger.info(f"Airport_id deleted successfully", airport_id=airport_id)
        except ObjectNotFoundException as ex:
            logger.warning("Failed to delete airport: Not Found", airport_id=airport_id)
            raise AirportNotFoundException from ex