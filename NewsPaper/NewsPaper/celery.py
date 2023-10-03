import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')
from datetime import timedelta
from celery.schedules import crontab

app.conf.beat_schedule = {
    'send-weekly-email': {
        'task': 'news.tasks.send_weekly_email',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
    },
}

app.autodiscover_tasks()
