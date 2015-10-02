# coding: utf-8

from os import environ

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

environ.setdefault('DJANGO_SETTINGS_MODULE', 'nobody.settings')

# via http://docs.celeryproject.org/en/latest/django/
mq = Celery('nobody')

mq.conf.update(
    CELERY_ACCEPT_CONTENT=['pickle'],
    CELERY_TIMEZONE=settings.TIME_ZONE,
    CELERY_RESULT_BACKEND=settings.CELERY_RESULT_BACKEND,
    CELERYD_LOG_COLOR=False,
    BROKER_URL=settings.CELERY_BROKER_URL,
    CELERY_SEND_TASK_ERROR_EMAILS=True,
    ADMINS=settings.ADMINS,
    SERVER_EMAIL=settings.SERVER_EMAIL,
    EMAIL_HOST=settings.EMAIL_HOST,
    CELERYBEAD_SCHEDULE={
        'arrage-items-for-users': {
            'task': 'tasks.arrange_items_for_users',
            'schedule': crontab(minute=0, hour=0)
        }
    }
)

mq.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
