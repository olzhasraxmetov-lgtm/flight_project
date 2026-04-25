from datetime import datetime
from decimal import Decimal

from app.core.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, Numeric, Enum, DateTime, func

from app.helpers.payment_status import PaymentStatus


class PaymentsORM(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"), nullable=False, index=True)
    transaction_id: Mapped[str] = mapped_column(String(70), nullable=False, unique=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[
        PaymentStatus] = mapped_column(Enum(PaymentStatus, native_enum=True))
    payment_method: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())