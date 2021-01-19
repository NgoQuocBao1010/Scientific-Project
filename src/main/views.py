from django.shortcuts import render


def home(request):
    context = {

    }

    return render(request, 'main/index.html', context)
