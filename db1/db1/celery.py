import os
from celery import Celery
from one.tasks import all2

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'db1.settings')

app = Celery('db1')

app.config_from_object('django.conf:settings', namespace='CELERY')

@app.task
def see_you():
    all2()
    print("See you in ten seconds!")


app.autodiscover_tasks(see_you)


app.conf.beat_schedule = {
    "see-you-in-ten-seconds-task": {
        "task": "one.tasks.all2",
        "schedule": 10.0,
    }

}