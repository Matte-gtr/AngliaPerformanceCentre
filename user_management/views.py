from django.shortcuts import render, reverse, redirect, get_object_or_404,\
    HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.core.mail import send_mail, BadHeaderError

from contact.models import Message, Callback
from testimonials.models import Review
from contact.forms import MessageResponseForm


def paginator_helper(request, object_list, per_page):
    paginator = Paginator(object_list, per_page)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return page_object

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
def admin_messages(request):
    """ a view to display the admin panel """
    # Safety features required
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=request.user.id)
    else:
        user = request.user
    if request.user.is_staff:
        message_count = Message.objects.filter(read=False).count
        message_pag = paginator_helper(request,
                                       Message.objects.
                                       all().order_by("responded", "read",
                                                      "-received_on"),
                                       10)
        callback_count = Callback.objects.filter(read=False).count
        review_count = Review.objects.filter(read=False).count
        template = "user_management/admin_messages.html"
        context = {
            'title': 'admin messages',
            'section': 'user_management',
            'site_messages': message_pag,
            'message_count': message_count,
            'callback_count': callback_count,
            'review_count': review_count,
            'my_user': user,
        }
        return render(request, template, context)
    else:
        messages.warning(request, "You don't have the required permissions to\
                         view this page")
        return redirect(reverse('home'))


@login_required
def admin_callbacks(request):
    """ a view to display the admin panel """
    # Safety features required
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=request.user.id)
    else:
        user = request.user
    if request.user.is_staff:
        message_count = Message.objects.filter(read=False).count
        callback_count = Callback.objects.filter(read=False).count
        callback_pag = paginator_helper(request,
                                        Callback.objects.
                                        all().order_by("responded", "read",
                                                       "-received_on"),
                                        10)
        review_count = Review.objects.filter(read=False).count
        template = "user_management/admin_callbacks.html"
        context = {
            'title': 'admin callbacks',
            'section': 'user_management',
            'message_count': message_count,
            'callbacks': callback_pag,
            'callback_count': callback_count,
            'review_count': review_count,
            'my_user': user,
        }
        return render(request, template, context)
    else:
        messages.warning(request, "You don't have the required permissions to\
                         view this page")
        return redirect(reverse('home'))


@login_required
def admin_reviews(request):
    """ a view to display the admin panel """
    # Safety features required
    if request.user.is_authenticated:
        user = get_object_or_404(User, pk=request.user.id)
    else:
        user = request.user
    if request.user.is_staff:
        message_count = Message.objects.filter(read=False).count
        callback_count = Callback.objects.filter(read=False).count
        review_count = Review.objects.filter(read=False).count
        review_pag = paginator_helper(request,
                                      Review.objects.
                                      filter(authorised=False).
                                      order_by("read", "-created_on"),
                                      10)
        template = "user_management/admin_reviews.html"
        context = {
            'title': 'admin reviews',
            'section': 'user_management',
            'message_count': message_count,
            'callback_count': callback_count,
            'review_count': review_count,
            'reviews': review_pag,
            'my_user': user,
        }
        return render(request, template, context)
    else:
        messages.warning(request, "You don't have the required permissions to\
                         view this page")
        return redirect(reverse('home'))


@login_required
def view_review(request, review_id):
    """ a view to display a users review for authorisation """
    if request.user.is_staff:
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
    else:
        messages.warning(request, "You don't have the required permissions to\
                         view this page")
        return redirect(reverse('home'))


@login_required
def view_message(request, message_id):
    """ a view to display a message recieved """
    form = MessageResponseForm(
        initial={'message_header':
                 'Re: Anglia Performance Centre Enquiry'})
    if request.user.is_staff:
        message = get_object_or_404(Message, pk=message_id)
        message.read = True
        message.save(update_fields=['read'])
        template = "user_management/view_message.html"
        context = {
            'title': 'message ' + str(message_id),
            'section': 'user_management',
            'form': form,
            'message': message,
        }
        return render(request, template, context)
    else:
        messages.warning(request, "You don't have the required permissions to\
                         view this page")
        return redirect(reverse('home'))


@login_required
def view_callback(request, callback_id):
    """ a view to display a users callback request """
    if request.user.is_staff:
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
    else:
        messages.warning(request, "You don't have the required permissions to\
                         view this page")
        return redirect(reverse('home'))


@login_required
def approve_review(request, review_id):
    """ a view to approve a users review so it will be displayed on the \
        testimonials page """
    if request.user.is_staff:
        review = get_object_or_404(Review, pk=review_id)
        review.authorised = True
        review.save(update_fields=['authorised'])
        messages.success(request, f"Review {review_id} has been authorised")
        return redirect(reverse('admin_reviews'))
    else:
        messages.warning(request, "You don't have the required permissions to\
                         approve reviews")
        return redirect(reverse('home'))


@login_required
def mark_unread(request, object_id, model):
    """ a view to mark an object as unread in the admin page """
    if model == 'review':
        this_object = get_object_or_404(Review, pk=object_id)
        this_path = redirect(reverse('admin_reviews'))
    elif model == 'callback':
        this_object = get_object_or_404(Callback, pk=object_id)
        this_path = redirect(reverse('admin_callbacks'))
    else:
        this_object = get_object_or_404(Message, pk=object_id)
        this_path = redirect(reverse('admin_messages'))

    this_object.read = False
    this_object.save(update_fields=['read'])
    this_object.save()
    return this_path


@login_required
def reply_to_message(request, message_id):
    """ a view to send a response to a message """
    if request.method == "POST":
        if request.user.is_staff:
            form = MessageResponseForm(request.POST or None)
            if form.is_valid():
                original_message = get_object_or_404(Message, pk=message_id)
                new_response = form.save(commit=False)
                new_response.response_to = original_message
                new_response.save()
                original_message.responded = True
                original_message.save(update_fields=['responded'])

                subject = form.cleaned_data['message_header']
                from_email = 'contact@apcperformance.co.uk'
                message = form.cleaned_data['message_body']
                recipient = original_message.email
                recipients = []
                recipients.append(recipient)

                try:
                    send_mail(subject, message, from_email, recipients)
                    messages.success(request, "Your response has been sent")
                except BadHeaderError:
                    HttpResponse('Bad Header Found')
                return redirect('view_message', message_id=message_id)
            else:
                messages.error(request, "Please check all fields are filled \
                               out and resend your response")
        else:
            messages.warning(request, "You do not have permissions to \
                             messages customers")
            return redirect(reverse('home'))
    else:
        return redirect(reverse('home'))
