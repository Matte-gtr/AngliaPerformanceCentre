from django.shortcuts import render


def cars(request):
    """ a view for the cars for sale page """
    template = 'shop/cars.html'
    context = {
        'title': 'cars for sale',
        'section': 'shop',
    }
    return render(request, template, context)


def parts(request):
    """ a view for the parts for sale page """
    template = 'shop/parts.html'
    context = {
        'title': 'parts for sale',
        'section': 'shop',
    }
    return render(request, template, context)
