from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from .forms import ReviewForm
from .models import ReviewImage, Review
from django.db.models import Avg


def testimonials(request):
    """ a view for the testimonials page """
    auth_reviews = Review.objects.filter(authorised=False)
    review_count = Review.objects.filter(authorised=False).count()
    average = Review.objects.filter(authorised=False).\
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


def post_review(request):
    """ a view for posting a review on the testimonials page """
    if request.method == "POST":
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
                messages.success(request, "Thanks for your review, it has been\
                     submitted")
                return redirect(reverse("testimonials"))
        else:
            messages.warning(request, "Please log in to post a review")
            return redirect(reverse("account_login"))
