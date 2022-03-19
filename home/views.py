from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Avg

from contact.forms import MessageForm, CallbackForm
from .models import Advert
from .forms import AdvertForm
from testimonials.models import Review


def home(request):
    """ a view for the home page """
    adverts = Advert.objects.all()
    reviews = Review.objects.filter(authorised=True).\
        order_by('-created_on')[:11]
    review_count = Review.objects.filter(authorised=True).count()
    average = Review.objects.filter(authorised=True).\
        aggregate(Avg('stars'))['stars__avg']
    if review_count > 0:
        average_rating = round(average, 1)
    else:
        average_rating = "No Ratings yet"
    for review in reviews:
        review.clip = review.review[:80]
    form = MessageForm(request.POST or None)
    miniform = CallbackForm(request.POST or None)
    template = 'home/home.html'
    context = {
        'title': 'home',
        'section': 'home',
        'adverts': adverts,
        'form': form,
        'miniform': miniform,
        'reviews': reviews,
        'review_count': review_count,
        'average_rating': average_rating,
    }
    return render(request, template, context)


@login_required
def add_advert(request):
    """ a view to add an advert """
    if request.user.is_staff:
        if request.method == "POST":
            form = AdvertForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, "Your advert has been saved")
                return redirect(reverse('admin_adverts'))
            messages.error(request, "Please check your form and \
                           re-submit")
        else:
            form = AdvertForm()
        template = 'home/add_advert.html'
        context = {
            'title': 'add advert',
            'section': 'home',
            'form': form,
        }
        return render(request, template, context)
    messages.warning(request, "You don't have the required \
        permissions to complete this action")
    return redirect(reverse('home'))


@login_required
def edit_advert(request, advert_id):
    """ a view to edit an advert """
    if request.user.is_staff:
        advert = get_object_or_404(Advert, pk=advert_id)
        if request.method == "POST":
            form = AdvertForm(request.POST, request.FILES, instance=advert)
            if form.is_valid():
                form.save()
                messages.success(request, "Your advert has been updated")
                return redirect(reverse('admin_adverts'))
            messages.error(request, "Please check your form and re-submit")
        else:
            form = AdvertForm(instance=advert)
        template = 'home/edit_advert.html'
        context = {
            'title': 'edit advert',
            'section': 'home',
            'form': form,
            'advert': advert,
        }
        return render(request, template, context)
    messages.warning(request, "You don't have the required \
        permissions to complete this action")
    return redirect(reverse('home'))


@login_required
def delete_advert(request, advert_id):
    """ a view to delete an advert """
    if request.user.is_staff:
        advert = get_object_or_404(Advert, pk=advert_id)
        try:
            advert.delete()
            messages.success(request, f'Advert for "{advert.name} deleted"')
        except Exception as err:
            messages.error(request, f'Delete advert "{advert.name}" \
                failed: {err}')
        return redirect(reverse('admin_adverts'))
    messages.warning(request, "You don't have the required \
        permissions to complete this action")
    return redirect(reverse('home'))
