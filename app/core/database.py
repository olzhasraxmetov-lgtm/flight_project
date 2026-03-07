from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

async_engine = create_async_engine(url=settings.DATABASE_URL, echo=False)
engine_null_pool = create_async_engine(url=settings.DATABASE_URL, poolclass=NullPool)
async_session_maker_null_poll = async_sessionmaker(bind=engine_null_pool, expire_on_commit=False)

AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


class Base(DeclarativeBase):
    pass