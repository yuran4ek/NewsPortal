import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

app = Celery('news')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.new_posts_per_week = {
    'send_email_about_new_posts_per_week': {
        'task': 'board.tasks.new_posts_per_week',
        'schedule': crontab(minute='*/2'),
    },
}

# crontab(hour=8, minute=0, day_of_week='monday')
