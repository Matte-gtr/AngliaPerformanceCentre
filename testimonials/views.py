from django.shortcuts import render
from .forms import ReviewForm, ReviewImagesForm


def testimonials(request):
    """ a view for the testimonials page """
    review_form = ReviewForm()
    review_images_form = ReviewImagesForm()
    template = "testimonials/testimonials.html"
    context = {
        'title': 'testimonials',
        'section': 'testimonials',
        'review_form': review_form,
        'review_images_form': review_images_form,
    }
    return render(request, template, context)


def post_review(request):
    """ a view for posting a review on the testimonials page """
    
