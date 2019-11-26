"""db1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from rest_framework import routers
from one import views
from django.urls import include, path




router = routers.DefaultRouter()
router.register(r'groups', views.ApiViewSet)
router.register(r'api2', views.SingleApi)



urlpatterns = [
    # url(r'^$', views.UsersListView.as_view(), name='users_list'),
    # url(r'^run/$', views.fun1, name='generate'),
    path('admin/', admin.site.urls),
    path('',views.FilterList2.as_view()),
    path('sun/',views.fun1),
    path('api2/', views.ClassicList.as_view()),
    url('^path/(?P<vin>.+)/$', views.FilterList.as_view()),
    path('path/', views.FilterList2.as_view()),


]

