from decimal import Decimal

from app.core.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship, column_property
from sqlalchemy import String, ForeignKey, DateTime, Numeric, Enum, Index, cast, CheckConstraint
from datetime import datetime
from typing import TYPE_CHECKING
from app.helpers.flight_status import FlightStatus
if TYPE_CHECKING:
    from app.models.seat_templates import SeamTemplatesORM
    from app.models.airports import AirportsORM
    from app.models.passengers import PassengersORM

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

    flight_status_str = column_property(cast(status, String))

    seat_template: Mapped["SeamTemplatesORM"] = relationship(
        "SeamTemplatesORM",
        back_populates="flight_instances"
    )

    departure_airport: Mapped['AirportsORM'] = relationship(
        'AirportsORM',
        foreign_keys=[departure_airport_id],
        back_populates='departing_instances',
    )

    arrival_airport: Mapped['AirportsORM'] = relationship(
        'AirportsORM',
        foreign_keys=[arrival_airport_id],
        back_populates='arrival_instances',
    )

    passengers: Mapped[list["PassengersORM"]] = relationship(
        "PassengersORM",
        back_populates="flight_instance"
    )

    __table_args__ = (
        Index("ix_flight_instances_departure_at", "departure_at"),
        Index("ix_flight_instances_arrival_at", "arrival_at"),
        Index("ix_flight_instances_departure_airport_id", "departure_airport_id"),
        CheckConstraint('arrival_at > departure_at', name='check_arrival_after_departure'),
    )

    def __str__(self):
        return f"Рейс: {self.flight_number}"