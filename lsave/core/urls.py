from django.urls import include, path
from . import views
from django.conf.urls import url
from django.contrib.auth import views as auth_views

#app_name = 'core'

urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('info', views.InfoPage.as_view(), name='info'),
    path('accounts', include('django.contrib.auth.urls')),
]
