from app.exceptions.base import AircraftNotFoundException, SeatTemplateNotFoundException
from app.services.base import BaseService
from app.schemas.seat_templates import SeatTemplateCreate

class SeatTemplatesService(BaseService):
    async def get_seat_template_or_404(self, seat_template_id: int):
        return await self.check_if_entity_exists(
            self.db.seat_templates,
            seat_template_id,
            SeatTemplateNotFoundException
        )

    async def create_seat_template(self, payload: SeatTemplateCreate):
        if payload.aircraft_model_id is not None:
            await self.check_if_entity_exists(self.db.aircrafts, payload.aircraft_model_id,
                                              error_exception=AircraftNotFoundException)

        seat_template = await self.db.seat_templates.add(payload)
        await self.db.commit()
        return seat_template

    async def get_all_seat_templates(self):
        return await self.db.seat_templates.get_all()

    async def get_seat_template_by_id(self, seat_template_id: int):
        return await self.get_seat_template_or_404(seat_template_id)