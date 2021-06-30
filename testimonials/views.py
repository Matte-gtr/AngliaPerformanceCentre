from django.shortcuts import render


def testimonials(request):
    """ a view for the testimonials page """
    template = "testimonials/testimonials.html"
    context = {
        'title': 'testimonials',
        'section': 'testimonials',
    }
    return render(request, template, context)
