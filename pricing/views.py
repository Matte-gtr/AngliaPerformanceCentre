from django.shortcuts import render


def pricing(request):
    """ a view for the pricing page """
    template = "pricing/pricing.html"
    context = {
        'title': 'pricing',
        'section': 'pricing',
    }
    return render(request, template, context)
