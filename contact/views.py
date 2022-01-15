from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render, HttpResponse, redirect, reverse
from django.contrib import messages
from django.http import HttpResponseRedirect

from .forms import MessageForm, CallbackForm


def contact(request):
    """ a view to display the contact page """
    form = MessageForm(request.POST or None)
    miniform = CallbackForm(request.POST or None)
    template = "contact/contact.html"
    context = {
        'title': 'contact',
        'section': 'contact',
        'form': form,
        'miniform': miniform,
    }
    return render(request, template, context)


def send_message(request):
    """ a view for sending a message to the garage """
    if request.method == "POST":
        page_location = request.POST.get('next', '/')
        form = MessageForm(request.POST or None)
        if form.is_valid():
            form.save()
            new_line = '\n'
            subject = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']
            if phone:
                final_message = f'Message from: {subject} ({from_email})\
                    {new_line}Phone: {phone}{new_line}{message}'
            else:
                final_message = f'Message from: {subject} ({from_email})\
                    {new_line}{message}'
            try:
                send_mail(subject, final_message, from_email,
                          ['contact@apcperformance.co.uk'])
            except BadHeaderError:
                HttpResponse('Bad Header Found')
            messages.success(request, 'Thanks for your message, \
                we will get back to you shortly')
            return HttpResponseRedirect(page_location)
        else:
            messages.error(request, "Message failed, please check \
                the form and resend")
            return HttpResponseRedirect(page_location)
    return redirect(reverse('home'))


def send_callback(request):
    """ a view for sending a callback request to the garage """
    if request.method == "POST":
        page_location = request.POST.get('next', '/')
        form = CallbackForm(request.POST or None)
        if form.is_valid():
            form.save()
            # Send SMS to be added
            messages.success(request, "Message Received, We will be \
                in touch shortly")
            return HttpResponseRedirect(page_location)
        else:
            messages.error(request, "Error, please check the form \
            and resend")
            return HttpResponseRedirect(page_location)
    return HttpResponseRedirect(page_location)
