from app.mappers.payments import PaymentsMapMapper
from app.models.payments import PaymentsORM
from app.repositories.base import BaseRepository


class PaymentsRepository(BaseRepository):
    model = PaymentsORM
    mapper = PaymentsMapMapper