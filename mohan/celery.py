import os 

from celery import Celery

from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mohan.settings')

app = Celery('mohan')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('HELLO FROM CELERY')

app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'send-notification-every-minute': {
        'task': 'send_notification',
        'schedule': crontab(minute='*/1'),
    }
}