from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import string, random

from .models import *
from realtime.models import Alert
from .forms import CarForm, CreateUserForm, ProfileForm, AddCarForm
from .customPrint import MyCustomPrint


# Welcome, Login, Register Page
def welcome(request):
    form = CreateUserForm()
    if request.user.is_authenticated:
        return redirect("home")

    formsErrors = []
    if request.method == "POST":
        if request.POST.get("login-username"):
            username = request.POST.get("login-username")
            password = request.POST.get("login-password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.info(request, "Email hoặc mật khẩu không hợp lệ")
        
        if request.POST.get("companyName"):
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()

            else:
                formsErrors = form.errors.values()
                form = CreateUserForm(None)

    context = {
        "errors": formsErrors,
    }
    return render(request, "welcome.html", context)

# Manage notifications
def getNotifications(company):
    lastestAlerts = Alert.objects.filter(drive__device__company=company).order_by('-timeOccured')[:5]
    
    unreadCounts = 0
    for alert in lastestAlerts:
        unreadCounts = (unreadCounts + 1) if not alert.isRead else unreadCounts
    
    return lastestAlerts, unreadCounts

# Home page
@login_required(login_url="/")
def home(request):
    company = request.user.profile.company
    cars = Car.objects.filter(company=company)
    
    form = AddCarForm(company=company)
    formsErrors = {}

    # Search filter
    searchKey = request.GET.get("search-key")

    if searchKey != '' and searchKey is not None:
        cars = cars.filter(licensePlate__icontains=searchKey)
    
    # Notifications manage
    lastestAlerts, unreadCounts = getNotifications(company)

    # Handle add more cars
    if request.method == "POST":
        carID = request.POST.get("device-id")

        # Edit Car Form
        if carID:
            editedCar = Car.objects.get(id=carID)
            form = CarForm(request.POST, instance=editedCar)
            if form.is_valid():
                form.save()
            else:
                # for err in form.errors:
                #     MyCustomPrint(err)
                pass

        # Add new car Form
        else:
            form = AddCarForm(request.POST, company=company)

            if form.is_valid():
                form.save()
                return redirect("home")

            else:
                for field in form:
                    for err in field.errors:
                        # print("Errors", field.label, err)
                        formsErrors.setdefault(field.label, err)
                form = AddCarForm()

    context = {
        "cars": cars, 
        "notifications": lastestAlerts, 
        "unreadNotis": unreadCounts, 
        "errors": formsErrors
    }
    return render(request, "home.html", context)


@login_required(login_url="/")
def logoutUser(request):
    logout(request)
    return redirect("welcome")


# Remove Cars
@login_required(login_url="/")
def removeCar(request, id):
    car = Car.objects.get(id=id)
    car.delete()
    return redirect("home")


# Account settings
@login_required(login_url="/")
def accountSettings(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
    
    # Notifications manage
    company = request.user.profile.company
    lastestAlerts, unreadCounts = getNotifications(company)
    context = {"profile": profile, "notifications": lastestAlerts, "unreadNotis": unreadCounts}
    return render(request, "account-setting.html", context)


@login_required(login_url="/")
def test(request):
    form = AddCarForm()

    if request.method == "POST":
        form = AddCarForm(request.POST)

        if form.is_valid():
            form.save(company=request.user.profile.company)
            return redirect("test")

    context = {"form": form}
    return render(request, "test.html", context)