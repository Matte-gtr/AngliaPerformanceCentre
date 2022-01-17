from django.shortcuts import render, reverse, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from contact.models import Message, Callback
from testimonials.models import Review


@login_required
def profile(request):
    """ a view to display a users profile """
    template = "user_management/profile.html"
    context = {
        'title': 'profile',
        'section': 'user_management',
    }
    return render(request, template, context)


@login_required
def admin_panel(request):
    """ a view to display the admin panel """
    # Pagination required
    # Safety features required
    if request.user.is_staff:
        site_messages = Message.objects.all().order_by("responded", "read",
                                                    "-received_on")
        callbacks = Callback.objects.all().order_by("responded", "read",
                                                    "-received_on")
        reviews = Review.objects.filter(authorised=False)
        template = "user_management/admin_panel.html"
        context = {
            'title': 'admin_panel',
            'section': 'user_management',
            'site_messages': site_messages,
            'callbacks': callbacks,
            'reviews': reviews,
        }
        return render(request, template, context)
    else:
        messages.warning(request, "You don't have the required permissions to\
                         view this page")
        return redirect(reverse('home'))


@login_required
def view_review(request, review_id):
    """ a view to display a users review for authorisation """
    review = get_object_or_404(Review, pk=review_id)
    review.read = True
    review.save(update_fields=['read'])
    template = "user_management/view_review.html"
    context = {
        'title': 'review ' + str(review_id),
        'section': 'user_management',
        'review': review,
    }
    return render(request, template, context)


@login_required
def view_message(request, message_id):
    """ a view to display a message recieved """
    message = get_object_or_404(Message, pk=message_id)
    message.read = True
    message.save(update_fields=['read'])
    template = "user_management/view_message.html"
    context = {
        'title': 'message ' + str(message_id),
        'section': 'user_management',
        'message': message,
    }
    return render(request, template, context)


@login_required
def view_callback(request, callback_id):
    """ a view to display a users callback request """
    callback = get_object_or_404(Callback, pk=callback_id)
    callback.read = True
    callback.save(update_fields=['read'])
    template = "user_management/view_callback.html"
    context = {
        'title': 'callback ' + str(callback_id),
        'section': 'user_management',
        'callback': callback,
    }
    return render(request, template, context)
