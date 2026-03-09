from app.core.database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, CHAR


class AirportsORM(Base):
    __tablename__ = "airports"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(CHAR(3), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    city: Mapped[str] = mapped_column(String(20), nullable=False)
    country: Mapped[str] = mapped_column(String(20), nullable=False)
    timezone: Mapped[str] = mapped_column(String(50), nullable=False)