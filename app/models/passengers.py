import typing
from decimal import Decimal

from app.core.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, ForeignKey, Numeric

if typing.TYPE_CHECKING:
    from app.models.bookings import BookingsORM
    from app.models.flight_instances import FlightInstancesORM

class PassengersORM(Base):
    __tablename__ = "passengers"

    id: Mapped[int] = mapped_column(primary_key=True)

    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)
    flight_instance_id: Mapped[int] = mapped_column(ForeignKey("flight_instances.id"), nullable=False)
    seat_instance_id: Mapped[int] = mapped_column(ForeignKey("seat_instances_map.id"), nullable=False, unique=True)

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    passport_number: Mapped[str] = mapped_column(String(20), nullable=False)

    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    booking: Mapped["BookingsORM"] = relationship(
        "BookingsORM",
        back_populates="passengers",
    )

    flight_instance: Mapped["FlightInstancesORM"] = relationship(
        "FlightInstancesORM",
        back_populates="passengers",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"