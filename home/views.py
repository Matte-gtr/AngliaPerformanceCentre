from django.shortcuts import render
from django.contrib import messages
from contact.forms import MessageForm
from .models import Advert


def home(request):
    """ a view for the home page """
    adverts = Advert.objects.all()
    form = MessageForm(request.POST or None)
    template = 'home/home.html'
    context = {
        'title': 'home',
        'section': 'home',
        'adverts': adverts,
        'form': form,
    }
    return render(request, template, context)
