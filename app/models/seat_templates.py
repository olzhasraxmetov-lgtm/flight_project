from app.core.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String, Boolean, ForeignKey


class SeamTemplatesORM(Base):
    __tablename__ = "seat_templates"

    id: Mapped[int] = mapped_column(primary_key=True)
    aircraft_model_id: Mapped[int] = mapped_column(ForeignKey("aircrafts.id"))
    name: Mapped[str] = mapped_column(String(60), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    aircraft: Mapped["AircraftsORM"] = relationship(
        "AircraftsORM",
        back_populates="templates",
    )