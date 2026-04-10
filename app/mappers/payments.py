from app.mappers.base import DataMapper
from app.models.payments import PaymentsORM
from app.schemas.payments import PaymentResponse

class PaymentsMapMapper(DataMapper):
    db_model = PaymentsORM
    schema = PaymentResponse
