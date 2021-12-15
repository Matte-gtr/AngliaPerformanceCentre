from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, HttpResponse, redirect, reverse
from .forms import MessageForm
from django.contrib import messages


def contact(request):
    """ a view to display the contact page """
    form = MessageForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            subject = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, from_email,
                          ['matt.snell.00@hotmail.co.uk'])
            except BadHeaderError:
                HttpResponse('Bad Header Found')
            messages.success(request, 'Thanks for your message, \
                we will get back to you shortly')
            return redirect(reverse('contact'))
    template = "contact/contact.html"
    context = {
        'title': 'contact',
        'section': 'contact',
        'form': form,
    }
    return render(request, template, context)
