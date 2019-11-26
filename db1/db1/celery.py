import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'db1.settings')

app = Celery('db1')

app.config_from_object('django.conf:settings')

@app.task
def see_you():
    print("See you in ten seconds!")


app.conf.beat_schedule = {
    "see-you-in-ten-seconds-task": {
        "task": "one.tasks.all",
        "schedule": 10.0,

    }

}