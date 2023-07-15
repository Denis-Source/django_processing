import os
from celery import Celery

from celery.signals import setup_logging

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
app = Celery(
    "core",
    include=['task.periodical']
)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
