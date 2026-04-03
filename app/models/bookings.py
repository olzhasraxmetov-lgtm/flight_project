import datetime
from decimal import Decimal

from app.core.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, Numeric, Enum, DateTime, func

from app.helpers.booking_status import BookingStatus


class BookingsORM(Base):
    __tablename__ = "bookings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    booking_reference: Mapped[str] = mapped_column(String(6), unique=True, nullable=False)
    total_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus, native_enum=True),
        default=BookingStatus.CREATED,
        server_default="CREATED"
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    passengers: Mapped[list["PassengersORM"]] = relationship(
        "PassengersORM",
        back_populates="booking",
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    @property
    def passengers_count(self) -> int:
        return len(self.passengers) if self.passengers else 0

    @property
    def flight_number(self) -> str | None:
        if self.passengers and self.passengers[0].flight_instance:
            return self.passengers[0].flight_instance.flight_number
        return None

    @property
    def departure_at(self):
        if self.passengers and self.passengers[0].flight_instance:
            return self.passengers[0].flight_instance.departure_at
        return None

    @property
    def arrival_at(self):
        if self.passengers and self.passengers[0].flight_instance:
            return self.passengers[0].flight_instance.arrival_at
        return None
