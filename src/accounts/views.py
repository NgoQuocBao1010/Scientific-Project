from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

import random
import string

from .models import *
from django.contrib.auth.models import User, Group

from .forms import ProfileForm, DriverForm, CarForm

from .decorators import adminOnly, rescritedProfile


# $$$$$$$$$$$$          Authentication          $$$$$$$$$$$$ #
def loginPage(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect("home")
            else:
                messages.info(request, "Username OR password is incorrect")

        context = {}
        return render(request, "accounts/login.html", context)


@login_required(login_url="login")
def logoutUser(request):
    logout(request)
    return redirect("login")


# $$$$$$$$$$$$          Home Page          $$$$$$$$$$$$ #
@login_required(login_url="login")
def home(request):
    context = {}
    return render(request, "accounts/home.html", context)


# $$$$$$$$$$$$          Create a user base on Profile          $$$$$$$$$$$$ #
def createUser(name, role="driver"):
    username = name.lower().replace(" ", "")

    password = ""
    upperLetter = 1

    while len(password) < 8:
        letterStatus = ["lower", "upper"]
        status = random.choice(letterStatus)

        if upperLetter > 2:
            status = "lower"

        if status == "upper":
            upperLetter += 1
            letter = random.choice(string.ascii_uppercase)
        else:
            letter = random.choice(string.ascii_lowercase)

        password += letter

    randomPos = random.randint(1, 7)
    randomNum = random.randint(0, 9)

    password = list(password)
    password[randomPos] = str(randomNum)
    password = "".join(password)

    user = User.objects.create_user(
        username=username, email="baoB1809677@student.ctu.edu.vn", password=password
    )
    user.save()

    group = Group.objects.get(name=role)
    user.groups.add(group)

    with open("userList.txt", "a+") as file:
        file.write(username + " " + password + "\n")

    return user


# $$$$$$$$$$$$          Users Management Page          $$$$$$$$$$$$ #
# Users Page
@login_required(login_url="login")
@adminOnly
def userPage(request):
    users = User.objects.all()

    context = {"users": users}
    return render(request, "accounts/users.html", context)


# Add an user to database (only accessable if user is admin)
@adminOnly
def addUserPage(request):
    form = ProfileForm()

    if request.method == "POST":
        form = ProfileForm(request.POST)

        if form.is_valid():
            name = request.POST.get("name")
            role = request.POST.get("role")

            try:
                user = createUser(name, role)
                profile = form.save()
                profile.user = user
                profile.save()

                if profile.role == "driver":
                    return redirect("driverInfo", str(profile.id))

                return redirect("users")

            except Exception as e:
                messages.error(request, str(e))

    context = {"form": form}
    return render(request, "accounts/addUser.html", context)


# Update driver Info
@adminOnly
def driverInfo(request, id):
    profile = Profile.objects.get(id=id)

    form = DriverForm()

    if request.method == "POST":
        form = DriverForm(request.POST)

        if form.is_valid():
            driver = form.save()
            driver.profile = profile
            driver.save()

            messages.success(request, f"Driver {profile.name} is created!!")

            return redirect("users")

    context = {"form": form}
    return render(request, "accounts/updateDrInfo.html", context)


# $$$$$$$$$$$$          Profile Page          $$$$$$$$$$$$ #
@rescritedProfile
def profilePage(request, id):
    profile = Profile.objects.get(id=id)

    context = {
        "profile": profile,
    }

    return render(request, "accounts/profile.html", context)


# Edit Profile
@rescritedProfile
def editProfile(request, id):
    profile = Profile.objects.get(id=id)

    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()

            messages.success(request, "Profile has been updated!!")
            return redirect("users")

    context = {
        "form": form,
    }

    return render(request, "accounts/editProfile.html", context)


# Delete User
def delUserPage(request, id):
    if request.method == "POST":
        profile = Profile.objects.get(id=id)
        deletedUser = profile.name

        user = profile.user
        user.delete()

        messages.success(request, f"User {deletedUser} is deleted")
        return redirect("users")

    context = {}

    return render(request, "accounts/deleteUser.html", context)


# $$$$$$$$$$$$          Car and Rasp Page          $$$$$$$$$$$$ #
def carsPage(request):
    cars = Car.objects.all()

    context = {"cars": cars}
    return render(request, "accounts/cars.html", context)


def addCarPage(request):
    form = CarForm()

    if request.method == "POST":
        form = CarForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(request, "Car has been added")
            return redirect("cars")

    context = {"form": form}
    return render(request, "accounts/addCar.html", context)


def updateCarPage(request, id):
    car = Car.objects.get(id=id)
    form = CarForm(instance=car)

    if request.method == "POST":
        form = CarForm(request.POST, instance=car)

        if form.is_valid():
            form.save()

            messages.success(request, f"Car {car} has been updated")
            return redirect("cars")

    context = {"form": form}
    return render(request, "accounts/updateCarInfo.html", context)


def deleteCar(request, id):
    delCar = Car.objects.get(id=id)
    delCar.delete()

    messages.success(request, f"Car {delCar} is deleted")

    return redirect("cars")


def raspsPage(request):
    rasps = RaspDevice.objects.all()

    context = {"rasps": rasps}
    return render(request, "accounts/rasps.html", context)