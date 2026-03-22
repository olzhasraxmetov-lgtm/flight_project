from app.exceptions.base import AircraftNotFoundException, ObjectNotFoundException
from app.schemas.aircrafts import AircraftCreate, AircraftUpdate
from app.services.base import BaseService
from loguru import logger

class AircraftsService(BaseService):
    async def get_aircraft_or_404(self, aircraft_id: int):
        return await self.check_if_entity_exists(
            self.db.aircrafts,
            aircraft_id,
            AircraftNotFoundException
        )

    async def create_aircraft(self, payload: AircraftCreate):
        new_aircraft = await self.db.aircrafts.add(payload)
        await self.db.commit()
        return new_aircraft

    async def get_aircrafts(self):
        return await self.db.aircrafts.get_all()

    async def get_aircraft_by_id(self, aircraft_id: int):
        return await self.get_aircraft_or_404(aircraft_id)

    async def _edit_aircraft(self, aircraft_id: int, payload: AircraftUpdate, exclude_unset):
        try:
            updated_aircraft = await self.db.aircrafts.edit(data=payload, exclude_unset=exclude_unset, id=aircraft_id)
            await self.db.commit()
            logger.info(f"Aircraft updated successfully", aircraft_id=aircraft_id,
                        updated_data=payload.model_dump(exclude_unset=True))
            return updated_aircraft
        except ObjectNotFoundException as ex:
            logger.warning("Failed to update aircraft: Not Found", aircraft_id=aircraft_id)
            raise AircraftNotFoundException from ex

    async def update_aircraft(self, aircraft_id: int, payload: AircraftUpdate):
        return await self._edit_aircraft(aircraft_id, payload, exclude_unset=False)

    async def partially_update_aircraft(self, aircraft_id: int, payload: AircraftUpdate):
        return await self._edit_aircraft(aircraft_id, payload, exclude_unset=True)

    async def delete_aircraft(self, aircraft_id: int):
        try:
            await self.db.aircrafts.delete(id=aircraft_id)
            await self.db.commit()
            logger.info(f"Aircraft deleted successfully", aircraft_id=aircraft_id)
        except ObjectNotFoundException as ex:
            logger.warning("Failed to delete aircraft: Not Found", aircraft_id=aircraft_id)
            raise AircraftNotFoundException from ex