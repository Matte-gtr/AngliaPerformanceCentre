from django.shortcuts import render
from contact.models import Message, Callback


def profile(request):
    """ a view to display a users profile """
    template = "user_management/profile.html"
    context = {
        'title': 'profile',
        'section': 'user_management',
    }
    return render(request, template, context)


def admin_panel(request):
    """ a view to display the admin panel """
    # Pagination required
    site_messages = Message.objects.all()
    callbacks = Callback.objects.all()
    template = "user_management/admin_panel.html"
    context = {
        'title': 'admin_panel',
        'section': 'user_management',
        'site_messages': site_messages,
        'callbacks': callbacks,
    }
    return render(request, template, context)
