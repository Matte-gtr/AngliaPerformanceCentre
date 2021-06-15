from django.shortcuts import render
from django.contrib import messages


def home(request):
    """ a view for the home page """
    template = 'home/home.html'
    messages.success(request, "The messages are working if you can see this")
    context = {
        'title': 'home',
        'section': 'home',
    }
    return render(request, template, context)
