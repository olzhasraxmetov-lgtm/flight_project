from datetime import datetime

from app.core.database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship, column_property
from sqlalchemy import String, DateTime, func, cast
from app.helpers.users_role import UserRoleEnum

class UsersORM(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    phone: Mapped[str] = mapped_column(String(50), unique=True)
    role: Mapped[str] = mapped_column(String(50), default=UserRoleEnum.USER, server_default="user", nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    bookings: Mapped[list["BookingsORM"]] = relationship(
        "BookingsORM",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    password: Mapped[str] = column_property(cast(None, String))

    user_role_str = column_property(cast(role, String))

    def __str__(self):
        return f"{self.email}"