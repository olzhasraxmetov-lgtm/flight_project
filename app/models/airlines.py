from app.core.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String



class AirlinesORM(Base):
    __tablename__ = "airlines"

    id: Mapped[int] = mapped_column(primary_key=True)
    iata_code: Mapped[str] = mapped_column(String(3), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)

    flights: Mapped[list['FlightsORM']] = relationship(
        'FlightsORM',
        back_populates='airline'
    )

    def __str__(self):
        return f"{self.name}"