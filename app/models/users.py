from datetime import datetime

from app.core.database import Base
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy import String, DateTime, func
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