from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def welcome(request):
    if request.method == "POST":
        username = request.POST.get("login-username")
        password = request.POST.get("login-password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Username OR password is incorrect")

    context = {}
    return render(request, "welcome.html", context)


@login_required(login_url="/")
def home(request):
    context = {}
    return render(request, "content.html", context)


def logoutUser(request):
    logout(request)
    return redirect("welcome")
