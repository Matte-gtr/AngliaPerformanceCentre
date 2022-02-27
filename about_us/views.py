from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import TeamMember
from .forms import TeamMemberForm


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
    members = TeamMember.objects.all().order_by('order')
    template = 'about_us/the_team.html'
    context = {
        'title': 'the team',
        'section': 'about',
        'members': members,
    }
    return render(request, template, context)


@login_required
def add_team_member(request):
    """ a view to add a new team member """
    if request.user.is_staff:
        form = TeamMemberForm(request.POST, request.FILES)
        if request.method == "POST":
            if form.is_valid():
                member = form.save(commit=False)
                member.order = 12
                member.save()
                messages.success(request, f"{member.first_name} \
                    {member.surname} added")
                return redirect(reverse('admin_members'))
            else:
                messages.error(request, "Please update your form and \
                    re-submit")
        else:
            form = TeamMemberForm()
        template = 'about_us/add_member.html'
        context = {
            'title': "add member",
            'section': 'about',
            'form': form,
        }
        return render(request, template, context)
    else:
        messages.warning(request, "You don't have the required \
            permissions to complete this action")
        return redirect(reverse('the_team'))


@login_required
def edit_team_member(request, member_id):
    """ a view to edit a team members details/photo """
    if request.user.is_staff:
        team_member = get_object_or_404(TeamMember, pk=member_id)
        fname = team_member.first_name
        lname = team_member.surname
        if request.method == "POST":
            form = TeamMemberForm(request.POST, request.FILES,
                                  instance=team_member)
            if form.is_valid():
                form.save()
                messages.success(request, f"{fname} {lname} updated")
                return redirect(reverse('admin_members'))
            else:
                messages.error(request, "Please check all field are filled out \
                    correctly and re-submit")
        else:
            form = TeamMemberForm(instance=team_member)
        template = "about_us/edit_member.html"
        context = {
            'title': 'edit member',
            'section': 'about',
            'form': form,
            'member': team_member,
        }
        return render(request, template, context)
    else:
        messages.warning(request, "You don't have the required \
            permissions to complete this action")
        return redirect(reverse('the_team'))


@login_required
def delete_team_member(request, member_id):
    """ a view to delete a team member """
    if request.user.is_staff:
        team_member = get_object_or_404(TeamMember, pk=member_id)
        fname = team_member.first_name
        lname = team_member.surname
        try:
            team_member.delete()
            messages.success(request, f"{fname} {lname} successfully deleted")
        except Exception as err:
            messages.error(request, f"error deleting team \
                           member: {err}")
        return redirect(reverse('admin_members'))
    else:
        messages.warning(request, "You don't have the required permissions \
            to complete this action")
        return redirect(reverse('the_team'))


def terms_and_conditions(request):
    """ a view for the terms and conditions page """
    template = 'about_us/terms_and_conditions.html'
    context = {
        'title': 'terms & conditions',
        'section': 'about',
    }
    return render(request, template, context)
