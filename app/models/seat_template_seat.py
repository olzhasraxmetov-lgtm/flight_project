from app.core.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship, column_property
from sqlalchemy import ForeignKey, CHAR, Enum, UniqueConstraint, Index, cast, String
from app.helpers.cabin_class import CabinClass
from app.helpers.seat_type import SeatType


class SeatTemplateSeatsORM(Base):
    __tablename__ = "seat_template_seats"

    id: Mapped[int] = mapped_column(primary_key=True)
    seat_template_id: Mapped[int] = mapped_column(ForeignKey("seat_templates.id", ondelete="CASCADE"), nullable=False)
    seat_number: Mapped[str] = mapped_column(CHAR(4), nullable=False)
    cabin_class: Mapped[CabinClass] = mapped_column(Enum(CabinClass, native_enum=True), nullable=False)
    seat_type: Mapped[SeatType] = mapped_column(Enum(SeatType, native_enum=True), nullable=False)
    row_number: Mapped[int] = mapped_column(nullable=False)
    seat_letter: Mapped[str] = mapped_column(CHAR(1), nullable=False)

    __table_args__ = (
        UniqueConstraint("seat_template_id", "seat_number", name="uq_st_seats_template_number"),
        Index("ix_st_seats_template_row_letter", "seat_template_id", "row_number", "seat_letter"),
    )

    template: Mapped["SeamTemplatesORM"] = relationship(
        "SeamTemplatesORM",
        back_populates="seats"
    )

    cabin_class_str = column_property(cast(cabin_class, String))
    seat_type_str = column_property(cast(seat_type, String))

    def __str__(self):
        return f"{self.seat_number} ({self.cabin_class.value if hasattr(self.cabin_class, 'value') else self.cabin_class})"