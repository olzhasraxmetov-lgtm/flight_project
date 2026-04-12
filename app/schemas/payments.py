from pydantic import BaseModel

from app.helpers.payment_status import PaymentStatus

class PaymentResponse(BaseModel):
    transaction_id: str
    status: PaymentStatus
    id: int
    booking_id: int