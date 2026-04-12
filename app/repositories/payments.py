from sqlalchemy import select

from app.mappers.payments import PaymentsMapMapper
from app.models.payments import PaymentsORM
from app.repositories.base import BaseRepository
from app.helpers.payment_status import PaymentStatus


class PaymentsRepository(BaseRepository):
    model = PaymentsORM
    mapper = PaymentsMapMapper

    async def get_payment(self, booking_id: int):
        stmt = (
            select(self.model)
            .where(
                self.model.booking_id == booking_id,
                self.model.status == PaymentStatus.SUCCEEDED,
            )
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()