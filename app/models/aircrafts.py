from app.core.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import String



class AircraftsORM(Base):
    __tablename__ = "aircrafts"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    manufacturer: Mapped[str] = mapped_column(String(30), nullable=False)

    templates: Mapped[list["SeamTemplatesORM"]] = relationship(
        "SeamTemplatesORM",
        back_populates="aircraft",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    def __str__(self):
        return f"{self.name}"