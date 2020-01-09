from django.urls import path
from . import views
from django.views.static import serve
from django.conf.urls import url


app_name = 'quote'

urlpatterns = [
    path("create", views.create_quote, name='create_quote'),
    path("detail/<int:id>", views.detail_quote, name='detail_quote'),
    path("ajax/", views.quoteAjax, name="ajax"),
]