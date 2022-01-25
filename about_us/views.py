from django.shortcuts import render

from .models import TeamMember


def about_us(request):
    """ a view for the about us page """
    template = 'about_us/about_us.html'
    context = {
        'title': 'about us',
        'section': 'about',
    }
    return render(request, template, context)


def the_team(request):
    """ a view for the team page """
    members = TeamMember.objects.all()
    template = 'about_us/the_team.html'
    context = {
        'title': 'the team',
        'section': 'about',
        'members': members,
    }
    return render(request, template, context)


def terms_and_conditions(request):
    """ a view for the terms and conditions page """
    template = 'about_us/terms_and_conditions.html'
    context = {
        'title': 'terms & conditions',
        'section': 'about',
    }
    return render(request, template, context)
