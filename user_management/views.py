import json

from django.shortcuts import render, reverse, redirect, get_object_or_404,\
    HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.core.mail import send_mail, BadHeaderError
from django.http import JsonResponse
from django.contrib.auth.models import User

from contact.models import Message, Callback
from testimonials.models import Review, ReviewImage
from blog.models import BlogPost, BlogPostVideo
from contact.forms import MessageResponseForm
from home.models import Advert
from about_us.models import TeamMember


def paginator_helper(request, object_list, per_page):
    """ helper function for pagination of querysets """
    paginator = Paginator(object_list, per_page)
    page_number = request.GET.get('page')
    page_object = paginator.get_page(page_number)
    return page_object


@login_required
def profile(request):
    """ a view to display a users profile """
    user = get_object_or_404(User, pk=request.user.id)
    template = "user_management/profile.html"
    context = {
        'title': 'profile',
        'section': 'user_management',
        'user': user,
    }
    return render(request, template, context)


def process_ids(request, item, action, id_final):
    """ handles the processing for admin ajax requests """
    count = 0
    result = ""
    for obj_id in id_final:
        if item == 'blog-post':
            obj = get_object_or_404(BlogPost, pk=obj_id)
        elif item == "message":
            obj = get_object_or_404(Message, pk=obj_id)
        elif item == "callback":
            obj = get_object_or_404(Callback, pk=obj_id)
        elif item == "review":
            obj = get_object_or_404(Review, pk=obj_id)
        elif item == "advert":
            obj = get_object_or_404(Advert, pk=obj_id)
        elif item == "member":
            obj = get_object_or_404(TeamMember, pk=obj_id)
        elif item == "user":
            obj = get_object_or_404(User, pk=obj_id)
        else:
            return {'count': count, 'result': result}
        if action == "delete":
            try:
                if hasattr(obj, "video"):
                    videos = obj.video.all()
                    if videos:
                        for vid in videos:
                            video = get_object_or_404(BlogPostVideo, pk=vid.pk)
                            try:
                                video.delete()
                                messages.success(request, "video deleted")
                            except Exception as err:
                                messages.error(request, f"error deleting blog \
                                    video: {err}")
                if hasattr(obj, "image") and item != "advert" and \
                        item != "member":
                    images = obj.image.all()
                    if images:
                        for img in images:
                            image = get_object_or_404(ReviewImage, pk=img.pk)
                            try:
                                image.delete()
                            except Exception as err:
                                messages.error(request, f"error deleting review \
                                    image: {err}")
                obj.delete()
                count += 1
                result = "deleted"
            except Exception as err:
                messages.error(request, f"Error deleting {item}: {err}")
        elif action == "publish":
            try:
                obj.publish = True
                obj.save(update_fields=['publish'])
                count += 1
                result = "published"
            except Exception as err:
                messages.error(request, f"Error publishing {item}: {err}")
        elif action == "read":
            try:
                obj.read = True
                obj.save(update_fields=['read'])
                count += 1
                result = "marked read"
            except Exception as err:
                messages.error(request, f"Error updating {item}: {err}")
        elif action == "unread":
            try:
                obj.read = False
                obj.save(update_fields=['read'])
                count += 1
                result = "marked unread"
            except Exception as err:
                messages.error(request, f"Error updating {item}: {err}")
        elif action == "respond":
            try:
                obj.responded = True
                obj.save(update_fields=['responded'])
                count += 1
                result = "marked responded"
            except Exception as err:
                messages.error(request, f"Error updating {item}: {err}")
        elif action == "unrespond":
            try:
                obj.responded = False
                obj.save(update_fields=['responded'])
                count += 1
                result = "marked unresponded"
            except Exception as err:
                messages.error(request, f"Error updating {item}: {err}")
        elif action == "approve":
            try:
                obj.authorised = True
                obj.save(update_fields=['authorised'])
                count += 1
                result = "approved"
            except Exception as err:
                messages.error(request, f"Error approving {item}: {err}")
        elif action == "staff":
            try:
                obj.is_staff = True
                obj.save(update_fields=['is_staff'])
                count += 1
                result = "marked as staff"
            except Exception as err:
                messages.error(request, f"Error marking {item}: {err}")
        elif action == "unstaff":
            try:
                obj.is_staff = False
                obj.save(update_fields=['is_staff'])
                count += 1
                result = "unmarked as staff"
            except Exception as err:
                messages.error(request, f"Error unmarking {item}: {err}")
        else:
            return {'count': count, 'result': result}
    return {'count': count, 'result': result}


@login_required
def admin_messages(request):
    """ a view to display the admin panel """
    if request.user.is_staff:
        if request.is_ajax():
            item = request.POST.get('item')
            action = request.POST.get('action')
            id_list = request.POST.get('id_list')  # [1, 2 ,3 ]
            id_object = json.loads(id_list)
            for key, value in id_object.items():
                id_final = value
            response = process_ids(request, item, action, id_final)
            count = response['count']
            result = response['result']
            data = {}
            data[item] = item
            data[action] = action
            data[id_list] = id_list
            if count > 1:
                messages.success(request, f"{count} {item}s {result}")
            else:
                messages.success(request, f"{count} {item} {result}")
            return JsonResponse(data)
        message_count = Message.objects.filter(read=False).count
        message_pag = paginator_helper(request,
                                    Message.objects.
                                    all().order_by("responded", "read",
                                                    "-received_on"),
                                    10)
        callback_count = Callback.objects.filter(read=False).count
        review_count = Review.objects.filter(read=False).count
        blog_count = BlogPost.objects.filter(publish=False).count
        advert_count = Advert.objects.all().count
        member_count = TeamMember.objects.all().count
        user_count = User.objects.all().count
        template = "user_management/admin_messages.html"
        context = {
            'title': 'admin messages',
            'section': 'user_management',
            'site_messages': message_pag,
            'message_count': message_count,
            'callback_count': callback_count,
            'review_count': review_count,
            'blog_count': blog_count,
            'advert_count': advert_count,
            'member_count': member_count,
            'user_count': user_count,
        }
        return render(request, template, context)
    messages.warning(request, "You don't have the required permissions to\
                        view this page")
    return redirect(reverse('home'))


@login_required
def admin_callbacks(request):
    """ a view to display the admin panel """
    if request.user.is_staff:
        if request.is_ajax():
            item = request.POST.get('item')
            action = request.POST.get('action')
            id_list = request.POST.get('id_list')  # [1, 2 ,3 ]
            id_object = json.loads(id_list)
            for key, value in id_object.items():
                id_final = value
            response = process_ids(request, item, action, id_final)
            count = response['count']
            result = response['result']
            data = {}
            data[item] = item
            data[action] = action
            data[id_list] = id_list
            if count > 1:
                messages.success(request, f"{count} {item}s {result}")
            else:
                messages.success(request, f"{count} {item} {result}")
            return JsonResponse(data)
        message_count = Message.objects.filter(read=False).count
        callback_count = Callback.objects.filter(read=False).count
        callback_pag = paginator_helper(request,
                                        Callback.objects.
                                        all().order_by("responded", "read",
                                                       "-received_on"),
                                        10)
        review_count = Review.objects.filter(read=False).count
        blog_count = BlogPost.objects.filter(publish=False).count
        advert_count = Advert.objects.all().count
        member_count = TeamMember.objects.all().count
        user_count = User.objects.all().count
        template = "user_management/admin_callbacks.html"
        context = {
            'title': 'admin callbacks',
            'section': 'user_management',
            'message_count': message_count,
            'callbacks': callback_pag,
            'callback_count': callback_count,
            'review_count': review_count,
            'blog_count': blog_count,
            'advert_count': advert_count,
            'member_count': member_count,
            'user_count': user_count,
        }
        return render(request, template, context)
    messages.warning(request, "You don't have the required permissions to\
                        view this page")
    return redirect(reverse('home'))


@login_required
def admin_reviews(request):
    """ a view to display the admin panel """
    if request.user.is_staff:
        if request.is_ajax():
            item = request.POST.get('item')
            action = request.POST.get('action')
            id_list = request.POST.get('id_list')
            id_object = json.loads(id_list)
            for key, value in id_object.items():
                id_final = value
            response = process_ids(request, item, action, id_final)
            count = response['count']
            result = response['result']
            data = {}
            data[item] = item
            data[action] = action
            data[id_list] = id_list
            if count > 1:
                messages.success(request, f"{count} {item}s {result}")
            else:
                messages.success(request, f"{count} {item} {result}")
            return JsonResponse(data)
        else:
            message_count = Message.objects.filter(read=False).count
            callback_count = Callback.objects.filter(read=False).count
            review_count = Review.objects.filter(read=False).count
            blog_count = BlogPost.objects.filter(publish=False).count
            advert_count = Advert.objects.all().count
            member_count = TeamMember.objects.all().count
            user_count = User.objects.all().count
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
                'blog_count': blog_count,
                'advert_count': advert_count,
                'member_count': member_count,
                'user_count': user_count,
            }
            return render(request, template, context)
    else:
        messages.warning(request, "You don't have the required permissions to\
                         view this page")
        return redirect(reverse('home'))


@login_required
def admin_blog_posts(request):
    """ a view to display a list of unpublished blog posts """
    if request.user.is_staff:
        if request.is_ajax():
            item = request.POST.get('item')  # blog-post
            action = request.POST.get('action')  # delete, publish
            id_list = request.POST.get('id_list')  # [1, 2 ,3 ]
            id_object = json.loads(id_list)
            for key, value in id_object.items():
                id_final = value
            response = process_ids(request, item, action, id_final)
            count = response['count']
            result = response['result']
            data = {}
            data[item] = item
            data[action] = action
            data[id_list] = id_list
            if count > 1:
                messages.success(request, f"{count} {item}s {result}")
            else:
                messages.success(request, f"{count} {item} {result}")
            return JsonResponse(data)
        message_count = Message.objects.filter(read=False).count
        callback_count = Callback.objects.filter(read=False).count
        review_count = Review.objects.filter(read=False).count
        blog_count = BlogPost.objects.filter(publish=False).count
        advert_count = Advert.objects.all().count
        member_count = TeamMember.objects.all().count
        user_count = User.objects.all().count
        blog_posts = paginator_helper(request,
                                        BlogPost.objects.
                                        filter(publish=False).
                                        order_by('-added_on'),
                                        10)
        template = "user_management/admin_blog_posts.html"
        context = {
            'title': 'admin blog posts',
            'section': 'user_management',
            'message_count': message_count,
            'callback_count': callback_count,
            'review_count': review_count,
            'blog_count': blog_count,
            'blog_posts': blog_posts,
            'advert_count': advert_count,
            'member_count': member_count,
            'user_count': user_count,
        }
        return render(request, template, context)
    messages.warning(request, "You don't have the required permissions to\
                        view this page")
    return redirect(reverse('home'))


@login_required
def admin_adverts(request):
    """ a view for the advert admin page """
    if request.user.is_staff:
        if request.is_ajax():
            item = request.POST.get('item')
            action = request.POST.get('action')
            id_list = request.POST.get('id_list')
            id_object = json.loads(id_list)
            for key, value in id_object.items():
                id_final = value
            response = process_ids(request, item, action, id_final)
            count = response['count']
            result = response['result']
            data = {}
            data[item] = item
            data[action] = action
            data[id_list] = id_list
            if count > 1:
                messages.success(request, f"{count} {item}s {result}")
            else:
                messages.success(request, f"{count} {item} {result}")
            return JsonResponse(data)
        message_count = Message.objects.filter(read=False).count
        callback_count = Callback.objects.filter(read=False).count
        review_count = Review.objects.filter(read=False).count
        blog_count = BlogPost.objects.filter(publish=False).count
        advert_count = Advert.objects.all().count
        member_count = TeamMember.objects.all().count
        user_count = User.objects.all().count
        adverts = paginator_helper(request, Advert.objects.all(), 10)
        template = "user_management/admin_adverts.html"
        context = {
            'title': 'admin adverts',
            'section': 'user_management',
            'message_count': message_count,
            'callback_count': callback_count,
            'review_count': review_count,
            'blog_count': blog_count,
            'adverts': adverts,
            'advert_count': advert_count,
            'member_count': member_count,
            'user_count': user_count,
        }
        return render(request, template, context)
    messages.warning(request, "You don't have the required permissions to\
                        view this page")
    return redirect(reverse('home'))


@login_required
def admin_members(request):
    """ a view for the member admin page """
    if request.user.is_staff:
        if request.is_ajax():
            item = request.POST.get('item')
            action = request.POST.get('action')
            id_list = request.POST.get('id_list')
            id_object = json.loads(id_list)
            for key, value in id_object.items():
                id_final = value
            response = process_ids(request, item, action, id_final)
            count = response['count']
            result = response['result']
            data = {}
            data[item] = item
            data[action] = action
            data[id_list] = id_list
            if count > 1:
                messages.success(request, f"{count} {item}s {result}")
            else:
                messages.success(request, f"{count} {item} {result}")
            return JsonResponse(data)
        message_count = Message.objects.filter(read=False).count
        callback_count = Callback.objects.filter(read=False).count
        review_count = Review.objects.filter(read=False).count
        blog_count = BlogPost.objects.filter(publish=False).count
        advert_count = Advert.objects.all().count
        member_count = TeamMember.objects.all().count
        user_count = User.objects.all().count
        members = paginator_helper(request,
                                   TeamMember.objects.
                                   all().order_by('order'),
                                   10)
        template = "user_management/admin_members.html"
        context = {
            'title': 'admin team members',
            'section': 'user_management',
            'message_count': message_count,
            'callback_count': callback_count,
            'review_count': review_count,
            'blog_count': blog_count,
            'members': members,
            'advert_count': advert_count,
            'member_count': member_count,
            'user_count': user_count,
        }
        return render(request, template, context)
    messages.warning(request, "You don't have the required permissions to\
                        view this page")
    return redirect(reverse('home'))


@login_required
def admin_users(request):
    """ a view for the user admin page """
    if request.user.is_staff:
        if request.is_ajax():
            item = request.POST.get('item')  # user
            action = request.POST.get('action')  # delete
            id_list = request.POST.get('id_list')  # [1, 2 ,3 ]
            id_object = json.loads(id_list)
            for key, value in id_object.items():
                id_final = value
            response = process_ids(request, item, action, id_final)
            count = response['count']
            result = response['result']
            data = {}
            data[item] = item
            data[action] = action
            data[id_list] = id_list
            if count > 1:
                messages.success(request, f"{count} {item}s {result}")
            else:
                messages.success(request, f"{count} {item} {result}")
            return JsonResponse(data)
        message_count = Message.objects.filter(read=False).count
        callback_count = Callback.objects.filter(read=False).count
        review_count = Review.objects.filter(read=False).count
        blog_count = BlogPost.objects.filter(publish=False).count
        advert_count = Advert.objects.all().count
        member_count = TeamMember.objects.all().count
        user_count = User.objects.all().count
        users = paginator_helper(request, User.objects.all(), 10)
        template = "user_management/admin_users.html"
        context = {
            'title': 'admin users',
            'section': 'user_management',
            'message_count': message_count,
            'callback_count': callback_count,
            'review_count': review_count,
            'blog_count': blog_count,
            'users': users,
            'advert_count': advert_count,
            'member_count': member_count,
            'user_count': user_count,
        }
        return render(request, template, context)
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
def toggle_responded(request, object_id, model):
    """ a view to mark an object as responded in the admin page """
    if model == 'callback':
        this_object = get_object_or_404(Callback, pk=object_id)
        this_path = redirect('view_callback', callback_id=object_id)
    else:
        this_object = get_object_or_404(Message, pk=object_id)
        this_path = redirect('view_message', message_id=object_id)

    if this_object.responded:
        this_object.responded = False
    else:
        this_object.responded = True
    this_object.save(update_fields=['responded'])
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
            messages.error(request, "Please check all fields are filled \
                            out and resend your response")
        else:
            messages.warning(request, "You don't have the required permissions to \
                             message customers")
            return redirect(reverse('home'))
    else:
        return redirect(reverse('home'))


@login_required
def delete_message(request, message_id):
    """ a view to delete a message and all of it's replies """
    if request.user.is_staff:
        message = get_object_or_404(Message, pk=message_id)
        try:
            message.delete()
            messages.success(request, f"Successfully deleted \
                             message {message_id}")
        except Exception as err:
            messages.error(request, f"error deleting image: {err}")
        return redirect(reverse('admin_messages'))
    messages.warning(request, "You don't have the required \
                        permissions to delete messages")
    return redirect(reverse('home'))


@login_required
def delete_callback(request, callback_id):
    """ a view to delete a callback and all of it's replies """
    if request.user.is_staff:
        callback = get_object_or_404(Callback, pk=callback_id)
        try:
            callback.delete()
            messages.success(request, f"Successfully deleted \
                             callback {callback_id}")
        except Exception as err:
            messages.error(request, f"error deleting image: {err}")
        return redirect(reverse('admin_callbacks'))
    messages.warning(request, "You don't have the required permissions to delete \
                        callbacks")
    return redirect(reverse('home'))
