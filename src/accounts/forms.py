from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import Car


class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = [
            "name",
            "licensePlate",
        ]


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super(CreateUserForm, self).save(commit=False)
        user.username = user.email

        if commit:
            user.save()
        
        return user
