import typing

from app.core.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, CHAR

if typing.TYPE_CHECKING:
    from app.models.flights import FlightsORM
    from app.models.flight_instances import FlightInstancesORM


class AirportsORM(Base):
    __tablename__ = "airports"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(CHAR(3), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    city: Mapped[str] = mapped_column(String(20), nullable=False)
    country: Mapped[str] = mapped_column(String(20), nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), nullable=False)

    departing_flights: Mapped[list['FlightsORM']] = relationship(
        'FlightsORM',
        foreign_keys="[FlightsORM.departure_airport_id]",
        back_populates='departure_airport',
    )

    arrival_flights: Mapped[list['FlightsORM']] = relationship(
        'FlightsORM',
        foreign_keys="[FlightsORM.arrival_airport_id]",
        back_populates='arrival_airport',
    )

    departing_instances: Mapped[list['FlightInstancesORM']] = relationship(
        "FlightInstancesORM",
        foreign_keys="[FlightInstancesORM.departure_airport_id]",
        back_populates='departure_airport',
    )

    arrival_instances: Mapped[list['FlightInstancesORM']] = relationship(
        "FlightInstancesORM",
        foreign_keys="[FlightInstancesORM.arrival_airport_id]",
        back_populates='arrival_airport',
    )

    def __str__(self):
        return f"{self.code} {self.city}"