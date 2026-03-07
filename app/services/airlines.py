from app.services.base import BaseService
from app.schemas.airlines import AirlineCreate

class AirlinesService(BaseService):
    async def create_airline(self, payload: AirlineCreate):
        new_airline = await self.db.airlines.add(payload)
        await self.db.commit()
        return new_airline