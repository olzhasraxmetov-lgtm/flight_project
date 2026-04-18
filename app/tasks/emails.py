import asyncio
from jinja2 import Environment, FileSystemLoader
import os
from loguru import logger
from email.message import EmailMessage
import aiosmtplib
from app.core.config import settings
from app.core.database import get_async_session_null_pool
from app.exceptions.base import ObjectNotFoundException, BookingNotFoundException
from app.repositories.bookings import BookingsRepository
from app.tasks.celery_app import celery_app
from app.utils.ticket_gen import generate_ticket_pdf

template_dir = os.path.join(os.path.dirname(__file__), '../templates/')
env = Environment(loader=FileSystemLoader(template_dir))

@celery_app.task(name="emails:send_email_after_payment")
def send_email_after_payment(booking_id):
    async def _logic():

        async with get_async_session_null_pool() as session:
            repo = BookingsRepository(session)

            try:
                booking = await repo.get_booking_for_email(booking_id)
            except ObjectNotFoundException:
                logger.info("Booking not found", booking_id=booking_id)
                raise BookingNotFoundException

            email_template = env.get_template("email/booking_confirmation.html")
            html_content = email_template.render(booking=booking)

            pdf_bytes = await asyncio.to_thread(generate_ticket_pdf, booking)

            res_status = str(booking.status)
            res_price = str(booking.total_price)

            message = EmailMessage()
            message["From"] = settings.SMTP_USER
            message["To"] = booking.user.email
            message["Subject"] = f"Ваш билет на рейс {booking.booking_reference}"

            message.set_content("Ваш билет во вложении.")
            message.add_alternative(html_content, subtype="html")
            message.add_attachment(
                pdf_bytes,
                maintype="application",
                subtype="pdf",
                filename=f"Ticket_{booking.booking_reference}.pdf"
            )
            try:
                await aiosmtplib.send(
                    message,
                    hostname=settings.SMTP_HOST,
                    port=settings.SMTP_PORT,
                    username=settings.SMTP_USER,
                    password=settings.SMTP_PASS,
                    use_tls=False,
                    start_tls=True,
                )
                logger.info(f"Email successfully sent to", email=booking.user.email)
            except Exception as e:
                logger.error(f"Failed to send email: {e}")

        return f'Status: {res_status}, total_price: {res_price}'
    return asyncio.run(_logic())