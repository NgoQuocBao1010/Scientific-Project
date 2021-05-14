from django.forms import ModelForm
from django import forms

from .models import RaspDevice, Car


class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = [
            "name",
            "licensePlate",
        ]