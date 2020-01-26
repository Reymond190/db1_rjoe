import datetime
from celery.schedules import crontab
import string
from googlegeocoder import GoogleGeocoder
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse
import json
from .models import ray
import requests

import time
from datetime import timedelta
import datetime
import pandas as pd
from pandas.io.json import json_normalize
import math

from celery.task import periodic_task
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

from celery import shared_task
from .models import Alert ,api1
import pytz


@shared_task
def random():
    i = Alert()
    time2 = datetime.datetime.now()
    i.time = time2
    i.save()


def get_dataframe(y1):
    df1 = json_normalize(y1["assetHistory"])
    return df1


def get_api():
    time2 = datetime.datetime.now()
    tz = pytz.timezone('Asia/Kolkata')
    time2 =  time2.astimezone(tz)
    print(time2)
    time1 = time2 + timedelta(seconds=-10)
    time1 = time1.strftime("%Y-%m-%d %H:%M:%S")
    time2 = time2.strftime("%Y-%m-%d %H:%M:%S")
    time1 = str(time1)
    time2 = str(time2)
    r1 = requests.get('https://lnt.tracalogic.co/api/ktrack/larsentoubro/' + time1 + '/' + time2,
                      auth=HTTPBasicAuth('admin', 'admin'))
    x1 = r1.json()
    x2 = json.dumps(x1)
    y1 = json.loads(x2)
    return y1


@shared_task
def all2():
    print('hello')




