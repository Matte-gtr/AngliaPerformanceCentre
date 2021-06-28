from django.shortcuts import render
from django.contrib import messages
from .models import Advert


def home(request):
    """ a view for the home page """
    adverts = Advert.objects.all()
    template = 'home/home.html'
    messages.success(request, "The messages are working if you can see this")
    context = {
        'title': 'home',
        'section': 'home',
        'adverts': adverts,
    }
    return render(request, template, context)
