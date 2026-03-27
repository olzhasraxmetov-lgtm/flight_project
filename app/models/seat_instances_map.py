from decimal import Decimal

from app.core.database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, ForeignKey, Numeric, Enum, UniqueConstraint
from app.helpers.cabin_class import CabinClass
from app.helpers.seat_status import SeatStatus
from app.helpers.seat_type import SeatType


class SeatInstancesMapORM(Base):
    __tablename__ = 'seat_instances_map'

    id: Mapped[int] = mapped_column(primary_key=True)
    flight_instance_id: Mapped[int] = mapped_column(
        ForeignKey("flight_instances.id", ondelete="CASCADE"),
        index=True
    )

    seat_number: Mapped[str] = mapped_column(String(5), nullable=False)
    row_number: Mapped[int] = mapped_column(nullable=False)
    seat_letter: Mapped[str] = mapped_column(String(1), nullable=False)
    cabin_class: Mapped[CabinClass] = mapped_column(
        Enum(CabinClass, native_enum=True, name="cabinclass", create_type=False),
        nullable=False
    )
    seat_type: Mapped[SeatType] = mapped_column(
        Enum(SeatType, native_enum=True, create_type=False),
        nullable=False
    )

    status: Mapped[SeatStatus] = mapped_column(
        Enum(SeatStatus, native_enum=True),
        default=SeatStatus.AVAILABLE
    )

    price_override: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)
    __table_args__ = (
        UniqueConstraint("flight_instance_id", "seat_number", name="uq_flight_seat"),
    )