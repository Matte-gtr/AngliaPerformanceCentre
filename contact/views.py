from django.shortcuts import render
from .forms import MessageForm


def contact(request):
    """ a view to display the contact page """
    form = MessageForm(request.POST or None)
    template = "contact/contact.html"
    context = {
        'title': 'contact',
        'section': 'contact',
        'form': form,
    }
    return render(request, template, context)
