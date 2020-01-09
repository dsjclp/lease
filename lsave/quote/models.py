from django.db import models
from django.contrib import admin
from django.conf import settings
try:
    from django.contrib.auth import get_user_model
except ImportError:
    from django.contrib.auth.models import User
else:
    User = settings.AUTH_USER_MODEL

class Schedule(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    saleprice = models.PositiveIntegerField(default=100000)
    rv = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.id)


class Step(models.Model):
    schedule = models.ForeignKey(Schedule,
        related_name="has_steps", on_delete=models.CASCADE)
    rank = models.PositiveSmallIntegerField(default=1)
    #amount = models.PositiveIntegerField(default=0)
    number = models.PositiveSmallIntegerField(default=24)
    MONTHLY = 0
    QUARTERLY = 3
    ANNUAL = 12
    PERIODICITY_CHOICES = [
        (MONTHLY, 'Months'),
        (QUARTERLY, 'Quarters'),
        (ANNUAL, 'Years'),
    ]
    periodicity = models.PositiveSmallIntegerField(
        choices=PERIODICITY_CHOICES,
        default=MONTHLY,)
    UNKNOWN = 0
    VALUE = 1
    MODE_CHOICES = [
        (UNKNOWN, 'Find'),
        (VALUE, 'Set value'),
    ]
    mode = models.PositiveSmallIntegerField(
        choices=MODE_CHOICES,
        default=UNKNOWN,)
    AMOUNT_CHOICES = [
        (0, 'Zero'),
        (2, '2% of financed amount'),
        (5, '5% of financed amount'),
    ]
    amount = models.PositiveSmallIntegerField(
        choices=AMOUNT_CHOICES,
        default=0,)