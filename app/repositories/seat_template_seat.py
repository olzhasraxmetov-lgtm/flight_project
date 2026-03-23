from sqlalchemy import select, delete

from app.mappers.seat_template_seats import SeatTemplateSeatsMapper
from app.repositories.base import BaseRepository
from app.models.seat_template_seat import SeatTemplateSeatsORM

class SeatTemplateSeatsRepository(BaseRepository):
    model = SeatTemplateSeatsORM
    mapper = SeatTemplateSeatsMapper

    async def get_ordered_and_filters_seats(self, template_id: int):
        query = (
            select(self.model)
            .where(self.model.seat_template_id == template_id)
            .order_by(self.model.row_number,
                      self.model.seat_letter)
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def delete_by_template_id(self, template_id: int):
        query = delete(self.model).where(self.model.seat_template_id == template_id)
        await self.session.execute(query)