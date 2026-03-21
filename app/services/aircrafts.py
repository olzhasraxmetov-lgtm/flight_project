from app.schemas.aircrafts import AircraftCreate
from app.services.base import BaseService

class AircraftsService(BaseService):
    async def create_aircraft(self, payload: AircraftCreate):
        new_aircraft = await self.db.aircrafts.add(payload)
        await self.db.commit()
        return new_aircraft

    async def get_aircrafts(self):
        return await self.db.aircrafts.get_all()