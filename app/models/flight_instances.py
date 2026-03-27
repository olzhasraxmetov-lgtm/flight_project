from decimal import Decimal

from app.core.database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, ForeignKey, DateTime, Numeric, Enum, Index
from datetime import datetime

from app.helpers.flight_status import FlightStatus


class FlightInstancesORM(Base):
    __tablename__ = 'flight_instances'

    id: Mapped[int] = mapped_column(primary_key=True)
    flight_number: Mapped[str] = mapped_column(String(12), nullable=False)
    seat_template_id: Mapped[int] = mapped_column(ForeignKey('seat_templates.id'))

    departure_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    arrival_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    departure_airport_id: Mapped[int] = mapped_column(ForeignKey("airports.id"))
    arrival_airport_id: Mapped[int] = mapped_column(ForeignKey("airports.id"))

    base_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    status: Mapped[FlightStatus] = mapped_column(Enum(FlightStatus, native_enum=True), default=FlightStatus.SCHEDULED)

    __table_args__ = (
        Index("ix_flight_instances_departure_at", "departure_at"),
        Index("ix_flight_instances_arrival_at", "arrival_at"),
        Index("ix_flight_instances_departure_airport_id", "departure_airport_id"),
    )