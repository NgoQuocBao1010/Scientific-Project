from .models import Car, Profile, Driver
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
