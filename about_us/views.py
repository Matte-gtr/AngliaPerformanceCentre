from django.shortcuts import render


def about_us(request):
    """ a view for the about us page """
    template = 'about_us/about_us.html'
    context = {
        'title': 'about us',
        'section': 'about us',
    }
    return render(request, template, context)


def the_team(request):
    """ a view for the team page """
    template = 'about_us/the_team.html'
    context = {
        'title': 'the team',
        'section': 'about us',
    }
    return render(request, template, context)


def finance_options(request):
    """ a view for the finance options page """
    template = 'about_us/finance_options.html'
    context = {
        'title': 'finance options',
        'section': 'about us',
    }
    return render(request, template, context)


def terms_and_conditions(request):
    """ a view for the terms and conditions page """
    template = 'about_us/terms_and_conditions.html'
    context = {
        'title': 'terms & conditions',
        'section': 'about us',
    }
    return render(request, template, context)
