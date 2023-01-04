import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SheepFish_test.settings")

app = Celery("SheepFish_test")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
