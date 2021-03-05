from django.http import HttpResponse
from django.shortcuts import redirect

from .models import Profile


# decorator to allowed only admin to view the page
def adminOnly(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == "admin":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse("<h1>You are not authorized to view this page</h1>")

    return wrapper_func


# Only allowed to view user's profile if the user is the owner of that profile
# Or an admin
def rescritedProfile(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        profile = Profile.objects.get(id=kwargs.get("id"))

        if request.user == profile.user or group == "admin":
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse(
                "<h1>You are only authorized to access your own profile</h1>"
            )

    return wrapper_func
