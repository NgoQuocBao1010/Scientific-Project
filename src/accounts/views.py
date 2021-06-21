from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import string, random

from .models import *
from realtime.models import Alert
from .forms import CarForm, CreateUserForm

# Welcome, Login, Register Page
def welcome(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        if (request.POST.get("login-username")):
            username = request.POST.get("login-username")
            password = request.POST.get("login-password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.info(request, "Username or Password is incorrect")
            
        
        if request.POST.get("company-name"):
            form = CreateUserForm(request.POST)
            if form.is_valid():
                user = form.save()

                try:
                    newCompanyName = request.POST.get("company-name")
                    characters = string.ascii_letters + string.digits
                    roomCode = ''.join(random.choice(characters) for i in range(10))

                    newComp = Company.objects.create(
                        name=newCompanyName,
                        roomCode=roomCode,
                    )

                    Profile.objects.create(
                        user=user,
                        company=newComp,
                        name=user.username,
                        role="admin",
                    )
                except Exception as e:
                    print(e)

            else:
                print(form.errors)

    context = {}
    return render(request, "welcome.html", context)

# Manage notifications
def getNotifications(company):
    lastestAlerts = Alert.objects.filter(drive__device__car__company=company).order_by('-timeOccured')[:5]
    
    unreadCounts = 0
    for alert in lastestAlerts:
        unreadCounts = (unreadCounts + 1) if not alert.isRead else unreadCounts
    
    return lastestAlerts, unreadCounts

# Home page
@login_required(login_url="/")
def home(request):
    company = request.user.profile.company
    cars = Car.objects.filter(company=company)

    # Search filter
    searchKey = request.GET.get("search-key")

    if searchKey != '' and searchKey is not None:
        cars = cars.filter(licensePlate__icontains=searchKey)
    

    # Notifications manage
    lastestAlerts, unreadCounts = getNotifications(company)

    # Handle add more cars
    if request.method == "POST":
        carID = request.POST.get("device-id")

        if carID:
            editedCar = Car.objects.get(id=carID)
            form = CarForm(request.POST, instance=editedCar)
            if form.is_valid():
                form.save()
        else:
            # freeRasp = RaspDevice.objects.filter(car=None)[0]
            form = CarForm(request.POST)

            raspName = request.POST.get("raspName")
            raspPass = request.POST.get("raspPass")

            if form.is_valid():
                newCar = form.save()

                newRasp = RaspDevice.objects.create(
                    name=raspName,
                    password=raspPass,
                    car=newCar
                )
                newRasp.save()

                newCar.company = company
                newCar.save()

        return redirect("home")

    context = {"cars": cars, "notifications": lastestAlerts, "unreadNotis": unreadCounts}
    return render(request, "content.html", context)


@login_required(login_url="/")
def logoutUser(request):
    logout(request)
    return redirect("welcome")


@login_required(login_url="/")
def driver(request):
    company = request.user.profile.company
    profiles = Profile.objects.filter(company=company).filter(role="driver")

    lastestAlerts, unreadCounts = getNotifications(company)
    
    context = {'profiles': profiles, "notifications": lastestAlerts, "unreadNotis": unreadCounts}
    return render(request, "driver.html", context)



# Remove Cars
@login_required(login_url="/")
def removeCar(request, id):
    car = Car.objects.get(id=id)
    car.delete()
    return redirect("home")
