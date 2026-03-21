from app.core.database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String



class AircraftsORM(Base):
    __tablename__ = "aircrafts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(30), nullable=False)