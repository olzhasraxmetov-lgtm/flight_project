from app.exceptions.base import AircraftNotFoundException, SeatTemplateNotFoundException, ObjectNotFoundException
from app.services.base import BaseService
from app.schemas.seat_templates import SeatTemplateCreate, SeatTemplateUpdate
from loguru import logger

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

    async def _edit_seat_template(self, seat_template_id: int, payload: SeatTemplateUpdate, exclude_unset):
        try:
            updated_seat_template = await self.db.seat_templates.edit(data=payload, exclude_unset=exclude_unset, id=seat_template_id)
            await self.db.commit()
            logger.info(f"Seat template updated successfully", seat_template_id=seat_template_id,
                        updated_data=payload.model_dump(exclude_unset=True))
            return updated_seat_template
        except ObjectNotFoundException as ex:
            logger.warning("Failed to update seat template: Not Found", seat_template_id=seat_template_id)
            raise SeatTemplateNotFoundException from ex

    async def update_seat_template(self, seat_template_id: int, payload: SeatTemplateUpdate):
        return await self._edit_seat_template(seat_template_id, payload, exclude_unset=False)

    async def partially_update_seat_template(self, seat_template_id: int, payload: SeatTemplateUpdate):
        return await self._edit_seat_template(seat_template_id, payload, exclude_unset=True)

    async def delete_seat_template(self, seat_template_id: int):
        try:
            await self.db.seat_templates.delete(id=seat_template_id)
            await self.db.commit()
            logger.info(f"Seat template deleted successfully", seat_template_id=seat_template_id)
        except ObjectNotFoundException as ex:
            logger.warning("Failed to delete seat template: Not Found", seat_template_id=seat_template_id)
            raise SeatTemplateNotFoundException from ex