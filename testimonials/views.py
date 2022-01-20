from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import ReviewForm
from .models import ReviewImage, Review

from datetime import datetime


def testimonials(request):
    """ a view for the testimonials page """
    auth_reviews = Review.objects.filter(authorised=True)
    review_count = Review.objects.filter(authorised=True).count()
    average = Review.objects.filter(authorised=True).\
        aggregate(Avg('stars'))['stars__avg']
    if review_count > 0:
        average_rating = round(average, 1)
    else:
        average_rating = "No Ratings yet"
    review_form = ReviewForm()
    template = "testimonials/testimonials.html"
    context = {
        'title': 'testimonials',
        'section': 'testimonials',
        'review_form': review_form,
        'reviews': auth_reviews,
        'review_count': review_count,
        'average_rating': average_rating,
    }
    return render(request, template, context)


@login_required
def post_review(request):
    """ a view for posting a review on the testimonials page """
    if request.user.is_authenticated:
        form = ReviewForm(request.POST, request.FILES)
        files = request.FILES.getlist('image')

        if form.is_valid():
            new_review = form.save(commit=False)
            new_review.user = request.user
            new_review.save()

            for file in files:
                img = ReviewImage(image=file)
                img.save()
                new_review.image.add(img)

            new_review.save()
            messages.success(request, 'Thanks for your review, it has been\
                    submitted for approval')
            return redirect(reverse("testimonials"))
    else:
        messages.warning(request, "Please log in to post a review")
        return redirect(reverse("account_login"))


@login_required
def delete_review(request, review_id):
    """ a view to delete a review """
    review = get_object_or_404(Review, pk=review_id)
    images = review.image.all()
    if request.user == review.user or request.user.is_staff:
        try:
            if images:
                for item in images:
                    image = get_object_or_404(ReviewImage, pk=item.pk)
                    try:
                        image.delete()
                    except Exception as e:
                        messages.error(request, f"error deleting image: {e}")
            review.delete()
            messages.success(request, 'Your review by has been successfully \
                             deleted')
        except Exception as e:
            messages.error(request, f'Error deleting review: {e}')
    else:
        messages.warning(request, 'You are only able to delete your own \
                         reviews')
    return redirect(reverse("testimonials"))


@login_required
def edit_review(request, review_id):
    """ a view to edit your review """
    review = get_object_or_404(Review, pk=review_id)
    if request.user == review.user or request.user.is_staff:
        if request.method == "POST":
            if request.user == review.user:
                form = ReviewForm(request.POST, request.FILES, instance=review)
                files = request.FILES.getlist('image')
                if form.is_valid:
                    delete_string = request.POST.get('imagecontrol')
                    delete_list = []
                    if delete_string:
                        delete_list = delete_string.split(",")
                    if delete_list:
                        for image_id in delete_list:
                            review_image = get_object_or_404(ReviewImage,
                                                             pk=image_id)
                            try:
                                review_image.delete()
                            except Exception as e:
                                messages.error(request, f"error deleting image: {e}")
                    form_review = form.save(commit=False)
                    form_review.updated_on = datetime.now()
                    form_review.authorised = False
                    form_review.save()
                    for file in files:
                        img = ReviewImage(image=file)
                        img.save()
                        review.image.add(img)
                    form.save()
                    messages.success(request, "Your Review has been \
                                     successfully updated awaiting approval")
                    return redirect(reverse('testimonials'))
                else:
                    messages.error(request, "Update failed, Please ensure all fields \
                                are filled in and re-submit")
            else:
                messages.warning(request, "You cannot edit someone elses \
                                 review")
                return redirect(reverse('testimonials'))
        else:
            form = ReviewForm(instance=review)
    else:
        messages.warning(request, "You can only make changes to posts you \
                         have created")
        return redirect(reverse('testimonials'))
    template = "testimonials/edit-review.html"
    context = {
        'review': review,
        'form': form,
        'title': 'edit review',
        'section': 'testimonials',
    }
    return render(request, template, context)
