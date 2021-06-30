from django.shortcuts import render


def contact(request):
    """ a view to display the contact page """
    template = "contact/contact.html"
    context = {
        'title': 'contact',
        'section': 'contact',
    }
    return render(request, template, context)
