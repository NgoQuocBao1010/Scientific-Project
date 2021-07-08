from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

from .models import Car, Profile, RaspDevice


class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = [
            "name",
            "licensePlate",
        ]


class AddCarForm(forms.Form):
    carName = forms.CharField(max_length=50)
    licensePlate = forms.CharField(max_length=20)
    rasPass = forms.CharField(max_length=8, min_length=8)

    def clean_carName(self):
        data = self.cleaned_data.get("carName")

        car = Car.objects.filter(name__iexact=data)

        if len(car) > 0:
            raise ValidationError("Tên xe đã tồn tại")
        
        return data
    
    def clean_licensePlate(self):
        data =  self.cleaned_data.get("licensePlate")

        car = Car.objects.filter(licensePlate__iexact=data)

        if len(car) > 0:
            raise ValidationError("Biển số xe đã tồn tại")
        
        return data
    

    def clean_rasPass(self):
        data =  self.cleaned_data.get("rasPass")

        rasp = RaspDevice.objects.filter(password__iexact=data)

        if len(rasp) == 0:
            raise ValidationError("Mật khẩu không tồn tại thiết bị")
        
        if rasp[0].car:
            raise ValidationError(f"Thiết bị đang thuộc về {rasp[0].car}")
        
        return data
    
    def save(self, commit=True, *args, **kwargs):
        company = kwargs.get("company")
        name = self.cleaned_data.get("carName")

        licensePlate = self.cleaned_data.get("licensePlate")
        rasPass = self.cleaned_data.get("rasPass")

        rasp = RaspDevice.objects.get(password__iexact=rasPass)
        newCar = Car.objects.create(name=name, licensePlate=licensePlate)

        print(rasp, newCar, company)
    








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


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'phone', 'address']

