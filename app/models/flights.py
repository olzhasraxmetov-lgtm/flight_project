from datetime import datetime
from decimal import Decimal

from sqlalchemy import String, ForeignKey, DateTime, Numeric, Index
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.core.database import Base


class FlightsORM(Base):
    __tablename__ = 'flights'

    id: Mapped[int] = mapped_column(primary_key=True)
    flight_number: Mapped[str] = mapped_column(String(12))
    departure_airport_id: Mapped[int] = mapped_column(ForeignKey('airports.id'))
    arrival_airport_id: Mapped[int] = mapped_column(ForeignKey('airports.id'))
    airline_id: Mapped[int] = mapped_column(ForeignKey('airlines.id'))
    departure_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    arrival_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    price: Mapped[Decimal] = mapped_column(Numeric(10,2), default=0.0)

    departure_airport: Mapped['AirportsORM'] = relationship(
        'AirportsORM',
        foreign_keys=[departure_airport_id],
        back_populates='departing_flights',
    )

    arrival_airport: Mapped['AirportsORM'] = relationship(
        'AirportsORM',
        foreign_keys=[arrival_airport_id],
        back_populates='arrival_flights',
    )

    airline: Mapped['AirlinesORM'] = relationship(
        'AirlinesORM',
        back_populates='flights'
    )

    __table_args__ = (
        Index("ix_flights_departure_at", "departure_at"),
        Index("ix_flights_arrival_at", "arrival_at"),
        Index("ix_flights_departure_airport_id", "arrival_airport_id"),
        Index("ix_flights_arrival_airport_id", "departure_airport_id"),
    )