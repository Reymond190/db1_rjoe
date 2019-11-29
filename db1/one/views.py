# import datetime
# import json
# from datetime import timedelta
#
#
import pytz

from .models import ray
from .serializers import GroupSerializer
from rest_framework import viewsets, generics
from django.shortcuts import render
# from django.utils.termcolors import background
# from pandas.io.json import json_normalize
# from pkg_resources.extern import names
# from requests.auth import HTTPBasicAuth
# from .models import vehicle
# import schedule
# import time
import datetime
from celery.schedules import crontab
import string
from googlegeocoder import GoogleGeocoder
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse
import json
from .models import ray
import requests
from django.db.models import Q
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
from .models import Alert

from django.contrib.auth.models import User
from django.contrib import messages
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import FormView
from django.shortcuts import redirect
from .forms import GenerateRandomUserForm
from rest_framework.views import APIView
from .tasks import random
# from celery.task.control import inspect
from .models import ray, api1
from rest_framework.response import Response
from rest_framework import status
from .serializers import GroupSerializer, Serialize2
# class UsersListView(ListView):
#     template_name = 'users_list.html'
#     model = User
#
#
# class GenerateRandomUserView(FormView):
#     template_name = 'generate_random_users.html'
#     form_class = GenerateRandomUserForm
#
#     def form_valid(self, form):
#         total = form.cleaned_data.get('total')
#         random.delay(total)
#         return redirect('users_list')


def home(request):
    return render(request,'home.html')


def fun1(request):
    r = get_api()
    d = get_dataframe(r)
    d1 = d

    a1 = api1.objects.get(No="1")
    po = ray.objects.all().count()
    df = d
    print(df.shape[0])
    df2 = df.loc[(df["engine"] == "ON") & (df["speed"] > 0)]  # RUNNING VEHICLES
    df3 = df.loc[(df["engine"] == "ON") & (df["speed"] == 0)]  # IDLE VEHICLES
    df4 = df.loc[(df["engine"] == "OFF") & (df["speed"] == 0)]  # STOP_VEHICLES
    a1.id = "1"
    a1.Total = str(po)
    a1.Running = str(df2.shape[0] + 1)
    a1.Idle = str(df3.shape[0] + 1)
    a1.Stop = str(df4.shape[0] + 1)
    a1.NoData = "temperarily unavailable"
    a1.No_of_geofence = "temperarily unavailable"
    a1.No_of_overspeed = "temperarily unavailable"
    a1.save()  # hello

    for i in range(d1.shape[0]):
        v2 = ray()
        d11 = d1['speed'].astype(int)
        if (ray.objects.filter(vin=d1['assetId'][i])):
            v3 = ray.objects.get(vin=d1['assetId'][i])
            if (str(d1['engine'][i]) == 'ON' and d11[i] > 0):  # running
                time1 = v3.running
                time1 = datetime.datetime.strptime(time1, '%H:%M:%S')
                x = time1 + timedelta(seconds=10)
                x = x.time()
                v3.running = str(x)  # changes existing running to updated time
                v3.endlocation = str(d1['latitude'][i]) + "," + str(d1['longitude'][i])
                v3.engine_current = "ON"
                if (d11[i] > v3.maxspeed):  # check maxspeed with currentspeed
                    v3.maxspeed = d11[i]
                if (str(d1['status'][i]) == 'OverSpeed'):
                    v3.overspeed = v3.overspeed + 1
                    v3.alert = v3.alert + 1

            elif (str(d1["engine"][i]) == "ON" and d11[i] == 0):
                time1 = datetime.datetime.strptime(v3.idle, '%H:%M:%S')
                x = time1 + timedelta(seconds=10)  # changes existing running to updated time
                x = x.time()
                v3.idle = str(x)
                v3.engine_current = "ON"
                v3.noidle = int(v3.noidle + 1)

            elif (str(d1["engine"][i]) == "OFF" and d11[i] == 0):  # stop
                v3.maxstop = v3.maxstop + 1
                time1 = datetime.datetime.strptime(v3.stop, '%H:%M:%S')
                x = time1 + timedelta(seconds=10)
                x = x.time()
                v3.stop = str(x)
                v3.engine_current = "OFF"

            else:
                print("Error")
            v3.average = round(v3.average + d11[i] / 2)
            v3.endodometer = float(v3.endodometer + float(d1['odometer'][i]))
            v3.No_of_iterations = v3.No_of_iterations + 1
            v3.distance = float(v3.distance + float(d1['odometer'][i]))
            v3.direction = str(d1['direction'][i])
            v3.latitude = str(d1['latitude'][i])
            v3.longitude = str(d1['longitude'][i])
            v3.save()

        else:
            v2.vin = d1['assetId'][i]
            time2 = datetime.datetime.now()
            tz = pytz.timezone('Asia/Kolkata')
            time2 = time2.astimezone(tz)
            v2.date = time2.date()
            v2.time = time2.time()
            v2.AssetCode = d1['AssetCode'][i]
            v2.deviceImeiNo = d1['deviceImeiNo'][i]
            v2.plateNumber = d1['plateNumber'][i]
            v2.No_of_iterations = 0
            v2.startlocation = str(d1['latitude'][i]) + ", " + str(d1['longitude'][i])
            v2.endlocation = str(d1['latitude'][i]) + ", " + str(d1['longitude'][i])
            v2.startodometer = float(d1['odometer'][i])
            v2.endodometer = float(d1['odometer'][i])
            v2.distance = float(d1['odometer'][i])
            if (str(d1['status'][i]) == 'Running' or str(d1['status'][i]) == 'Overspeed'):
                v2.running = "00:00:10"
                v2.stop = "00:00:00"
                v2.engine_current = "ON"
                v2.idle = "00:00:00"
            elif (str(d1['status'][i]) == 'Stop'):
                v2.stop = "00:00:10"
                v2.running = "00:00:00"
                v2.engine_current = "OFF"
                v2.idle = "00:00:00"
            else:
                v2.running = "00:00:00"
                v2.engine_current = "ON"
                v2.stop = "00:00:00"
                v2.idle = "00:00:10"

            v2.current_speed = d11[i]
            v2.inactive = 0
            v2.noidle = 0
            v2.maxstop = 0
            v2.maxspeed = d11[i]
            v2.average = d11[i]
            v2.overspeed = 0
            v2.alert = 0
            v2.direction = str(d1['direction'][i])
            v2.latitude = str(d1['latitude'][i])
            v2.longitude = str(d1['longitude'][i])
            v2.No_of_iterations = 0
            v2.save()
            print("saved")

    return render(request, 'generate_random_users.html')

# class ApiList(APIView):
#
#     def get(self, request):
#         g = ray.objects.all()
#         serializer=GroupSerializer(g)
#         return Response(serializer.data)


class ApiViewSet(viewsets.ModelViewSet):
    queryset = ray.objects.all()
    serializer_class = GroupSerializer

class SingleApi(viewsets.ModelViewSet):
    queryset = api1.objects.all()
    serializer_class = Serialize2

def get_dataframe(y1):
    df1 = json_normalize(y1["assetHistory"])
    return df1


def get_api():
    time2 = datetime.datetime.now()
    print(time2)
    time1 = time2 + timedelta(seconds=-10)
    time1 = time1.strftime("%Y-%m-%d %H:%M:%S")
    time2 = time2.strftime("%Y-%m-%d %H:%M:%S")
    time1 = str(time1)
    time2 = str(time2)
    print(time2)
    r1 = requests.get('https://lnt.tracalogic.co/api/ktrack/larsentoubro/' + time1 + '/' + time2,
                      auth=HTTPBasicAuth('admin', 'admin'))
    x1 = r1.json()
    print(x1)
    x2 = json.dumps(x1)
    y1 = json.loads(x2)
    return y1


class FilterList(generics.ListAPIView):
    serializer_class = GroupSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        username = " "
        lol = " "
        username = self.kwargs['vin']
        lol = self.kwargs['vin']

        p = ray.objects.filter(Q(vin=username)|Q(plateNumber=lol))

        return p

class FilterList2(generics.ListAPIView):
    serializer_class = GroupSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        p = ray.objects.all()
        return p


class ClassicList(generics.ListAPIView):
    serializer_class = Serialize2

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        p = api1.objects.all()
        return p
