from django import forms
from django.forms import (formset_factory, modelformset_factory)
from .models import (Schedule, Step)

class ScheduleModelForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ('saleprice', 'rv')
        labels = {
            'saleprice': 'Financed amount €',
            'rv': 'Residual Value €',
        }
        widgets = {
                'saleprice': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Financed amount',
                'type':'range', 'step': '10000', 'min': '10000', 'max': '500000',
                'name': 'saleprice',
                'id': 'saleprice'
                }),
                'rv': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Residual Value amount',
                'type':'range', 'step': '1000', 'min': '0', 'max': '50000',
                'name': 'rv',
                'id': 'rv'
                }),
        }

StepFormset = modelformset_factory(
    Step,
    fields=('mode', 'number', 'periodicity', 'amount'),
    extra=1,
)