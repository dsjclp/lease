from django.urls import path
from . import views
from django.views.static import serve
from django.conf.urls import url


app_name = 'dashboard'

urlpatterns = [
    path('quote_list', views.ScheduleList.as_view(), name='quote_list'),
]