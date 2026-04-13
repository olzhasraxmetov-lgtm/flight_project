from loguru import logger

from app.core.database import get_async_session_null_pool

from app.helpers.booking_status import BookingStatus
from app.tasks.celery_app import celery_app
import asyncio
from app.repositories.bookings import BookingsRepository

@celery_app.task(name="cleanup_expired_bookings")
def cleanup_expired_bookings():
    async def _logic():


        async with get_async_session_null_pool() as session:
            repo = BookingsRepository(session)
            expired_bookings = await repo.get_expired_bookings()

            if not expired_bookings:
                logger.info("No found expired bookings")
                return

            for booking in expired_bookings:
                 booking.status = BookingStatus.CANCELLED

            await session.commit()
            logger.info(f"Successfully cancelled {len(expired_bookings)} bookings")
    return asyncio.run(_logic())

