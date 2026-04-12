from celery import Celery

from app.core.config import settings

celery_app = Celery('flight_tasks', broker=settings.REDIS_URL,backend=settings.REDIS_URL)

celery_app.autodiscover_tasks(['app.tasks'])

celery_app.conf.update(
    task_ignore_result=False,
    result_persistent=True,
)

celery_app.conf.beat_schedule = {
    "clean-up_every-5-minutes": {
        "task": "cleanup_expired_bookings",
        'schedule': 900.0,
    }
}