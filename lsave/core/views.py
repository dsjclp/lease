from django.views import generic
from django.utils import timezone
from blog.models import Post
from django.contrib import messages

from django.http import HttpResponse


class HomePage(generic.TemplateView):
    template_name = "core/home.html"


class InfoPage(generic.TemplateView):
    template_name = "core/info.html"
    