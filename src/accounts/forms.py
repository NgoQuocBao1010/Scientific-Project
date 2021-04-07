from .models import Car, Profile, Driver, RaspDevice
from django.forms import ModelForm


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = "__all__"
        exclude = ["user"]


class DriverForm(ModelForm):
    class Meta:
        model = Driver
        fields = "__all__"
        exclude = ["profile"]


class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = "__all__"


class RaspDeviceForm(ModelForm):
    class Meta:
        model = RaspDevice
        fields = "__all__"
