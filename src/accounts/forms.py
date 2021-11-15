from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse
from django.core.exceptions import ValidationError
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

import random, string
from datetime import datetime

from .models import Car, Profile, RaspDevice, Company
from realtime.models import Drive
from .customPrint import MyCustomPrint


class CarForm(ModelForm):
    class Meta:
        model = Car
        fields = [
            "name",
            "licensePlate",
        ]


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'phone', 'address']


class AddCarForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.company = kwargs.pop('company', None)
        super(AddCarForm, self).__init__(*args, **kwargs)
    
    carName = forms.CharField(max_length=50)
    licensePlate = forms.CharField(max_length=20)
    rasID = forms.CharField(max_length=8)
    rasPass = forms.CharField(max_length=8, min_length=8)

    def clean_carName(self):
        data = self.cleaned_data.get("carName")
        car = Car.objects.filter(name__iexact=data, company=self.company)

        if len(car) > 0:
            raise ValidationError("Tên xe đã tồn tại")
        
        return data
    
    def clean_licensePlate(self):
        data =  self.cleaned_data.get("licensePlate")
        car = Car.objects.filter(licensePlate__iexact=data)

        if len(car) > 0:
            raise ValidationError("Biển số xe đã tồn tại")
        
        return data

    def clean_rasID(self):
        data =  self.cleaned_data.get("rasID")

        rasp = RaspDevice.objects.filter(id=data)

        if rasp[0].company and rasp[0].company != self.company:
            raise ValidationError(f"Thiết bị không thuộc sở hữu của công ty bạn")

        if len(rasp) == 0:
            raise ValidationError("Không tồn tại thiết bị")
        
        if rasp[0].car:
            raise ValidationError(f"Thiết bị đã kết nối với xe khác")
        
        return data
    
    def clean_rasPass(self):
        data =  self.cleaned_data.get("rasPass")
        inputId = self.cleaned_data.get("rasID")

        try:
            password = RaspDevice.objects.get(id=inputId).password

            if password != data:
                raise ValidationError(f"Mật khẩu thiết bị không đúng")

        except RaspDevice.DoesNotExist:
            pass
        
        return data
            
    def save(self):
        name = self.cleaned_data.get("carName")
        licensePlate = self.cleaned_data.get("licensePlate")
        rasPass = self.cleaned_data.get("rasPass")

        rasp = RaspDevice.objects.get(password__iexact=rasPass)
        roomCode = "general" if not rasp.company else rasp.company.roomCode
        newCar = Car.objects.create(name=name, licensePlate=licensePlate, company=self.company)

        rasp.car = newCar
        rasp.company = self.company
        rasp.save()

        message = {
            "piDeviceID": rasp.id,
            "command": "getRoomCode",
            "roomCode": self.company.roomCode,
        }

        layer = get_channel_layer()
        async_to_sync(layer.group_send)(
            roomCode, {"type": "randomFunc", "message": message}
        )

        MyCustomPrint(f"Connection {rasp.name} => {newCar} => {self.company}, a signal is sent to general room", style="success")
    

class CreateUserForm(forms.Form):
    companyName = forms.CharField(max_length=50)
    email = forms.EmailField(max_length=50)
    password1 = forms.CharField(max_length=50)
    password2 = forms.CharField(max_length=50)

    def generateCompanyRoomCode(self):
        # Contains low, upper case and digit
        characters = string.ascii_letters + string.digits
        roomCode = ''.join(random.choice(characters) for i in range(10))

        return roomCode

    def clean_companyName(self):
        data =  self.cleaned_data.get("companyName")
        company = Company.objects.filter(name__iexact=data)

        if company:
            raise ValidationError(f"Tên công ty đã tồn tại")
        
        return data

    def clean_email(self):
        data =  self.cleaned_data.get("email")
        user = User.objects.filter(username__iexact=data) | User.objects.filter(email__iexact=data)

        if user:
            raise ValidationError(f"Email không hợp lệ")
        
        return data

    def clean_password1(self):
        password1 =  self.cleaned_data.get("password1")

        if len(password1) < 5:
            raise ValidationError(f"Mật khẩu quá ngắn")
        
        containsNum = any(letter.isdigit() for letter in password1)
        containsUppercase = any(letter.isupper() for letter in password1)

        if not containsNum or not containsUppercase:
            raise ValidationError(f"Mật khẩu cần chứa chữ hoa và chữ số")
            
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password2 =  cleaned_data.get("password2")
        password1 =  cleaned_data.get("password1")


        if password2 != password1:
            raise ValidationError(f"Mật khẩu không trùng khớp")

    
    def save(self):
        email =  self.cleaned_data.get("email")
        password1 =  self.cleaned_data.get("password1")

        user = User.objects.create_user(username=email, email=email)
        user.set_password(password1)
        user.save()

        newCompanyName =  self.cleaned_data.get("companyName")
        roomCode = self.generateCompanyRoomCode()

        newCom = Company.objects.create(
            name=newCompanyName,
            roomCode=roomCode,
        )

        Profile.objects.create(
            user=user,
            company=newCom,
            name=user.username,
        )

        MyCustomPrint(f"Reigister successfully {user}, {password1} and {newCom}", style="success")
        return user
    
    


    