from django.db import models

# Create your models here.
class Alert(models.Model):
    alert_name = models.CharField(null = True,max_length=100)
    vehicle_id = models.CharField(null = True,max_length=100)
    alert_type = models.CharField(null = True,max_length=100)
    priority = models.CharField(null = True,max_length=100)
    contact_no = models.CharField(null = True,max_length=100)
    action = models.CharField(null = True,max_length=100)
    latitude = models.CharField(null = True,max_length=100)
    longtude = models.CharField(null = True,max_length=100)
    time = models.CharField(null=True, max_length=100)

class ray(models.Model):
    vin = models.CharField(max_length=20, null=True)
    date = models.CharField(max_length=10,null=True)
    time = models.CharField(max_length=10, null=True)
    startlocation = models.TextField(max_length=100, null=True)
    startodometer = models.FloatField(max_length=10, null=True)
    running = models.CharField(max_length=10, null=True)
    idle = models.CharField(max_length=50, null=True)
    stop = models.CharField(max_length=10, null=True)
    inactive = models.CharField(max_length=10, null=True)
    endodometer = models.FloatField(max_length=10, null=True)
    endlocation = models.CharField(max_length=10, null=True)
    distance = models.FloatField(max_length=10, null=True)
    average = models.IntegerField(null=True)
    current_speed = models.IntegerField( null=True)
    maxstop = models.IntegerField( null=True)      #remove
    maxspeed = models.IntegerField( null=True)
    overspeed = models.IntegerField( null=True)
    alert = models.IntegerField( null=True)
    noidle = models.IntegerField(null=True)
    AssetCode = models.CharField(max_length=10, null=True)
    deviceImeiNo = models.CharField(max_length=15, null=True)
    plateNumber = models.CharField(max_length=10, null=True)
    No_of_iterations = models.IntegerField(null=True)
    latitude = models.CharField(max_length=10, null=True)
    longitude = models.CharField(max_length=10, null=True)
    direction = models.CharField(max_length=10, null=True)
    engine_current = models.CharField(max_length=10, null=True)


class api1(models.Model):
    Total = models.CharField(max_length=20, null=True)
    Running = models.CharField(max_length=20, null=True)
    Idle = models.CharField(max_length=20, null=True)
    Stop = models.CharField(max_length=20, null=True)
    NoData = models.CharField(max_length=20, null=True)
    vin = models.CharField(max_length=20, null=True)
    No_of_overspeed = models.CharField(max_length=20, null=True)
    No_of_geofence = models.CharField(max_length=20, null=True)


