from app.exceptions.base import AircraftNotFoundException
from app.schemas.aircrafts import AircraftCreate
from app.services.base import BaseService

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