from django.shortcuts import render


def profile(request):
    """ a view to display a users profile """
    template = "user_management/profile.html"
    context = {
        'title': 'profile',
    }
    return render(request, template, context)
