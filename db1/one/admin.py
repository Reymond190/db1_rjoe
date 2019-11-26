from django.contrib import admin

# Register your models here.
from .models import Alert
from .models import ray , api1

admin.site.register(ray)

admin.site.register(Alert)

admin.site.register(api1)