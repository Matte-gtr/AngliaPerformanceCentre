from django.shortcuts import render
from django.contrib import messages
from contact.forms import MessageForm, CallbackForm
from .models import Advert


def home(request):
    """ a view for the home page """
    adverts = Advert.objects.all()
    form = MessageForm(request.POST or None)
    miniform = CallbackForm(request.POST or None)
    template = 'home/home.html'
    context = {
        'title': 'home',
        'section': 'home',
        'adverts': adverts,
        'form': form,
        'miniform': miniform,
    }
    return render(request, template, context)
