from django.shortcuts import render


def cart(request):
    """ a view to display the shopping cart """
    template = "cart/cart.html"
    context = {
        'title': 'cart',
    }
    return render(request, template, context)
