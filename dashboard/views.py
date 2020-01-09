from django.views import generic
from quote.models import Schedule
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail

class ScheduleList(generic.ListView):
    queryset = Schedule.objects.all()
    template_name = 'dashboard/quote_list.html'