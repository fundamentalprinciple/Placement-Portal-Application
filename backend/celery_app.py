from celery import Celery
from application.config import Config
from celery.schedules import crontab

celery = Celery(
    "placement_portal",
    broker_url=Config.CELERY_BROKER_URL,
    result_backend=Config.CELERY_RESULT_BACKEND,
    include=["application.tasks"]
)

celery.conf.update(
    result_expires=3600,
    timezone="Asia/Kolkata",
    beat_schedule={
        "send-daily-reminders": {
            "task": "application.tasks.send_daily_reminders",
            "schedule": crontab(hour=19, minute=39),
        },
    },
)
