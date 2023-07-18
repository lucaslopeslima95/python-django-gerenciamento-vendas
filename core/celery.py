import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
app = Celery('core')
app.conf.broker_url = 'amqp://guest:guest@localhost:5672//'
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

