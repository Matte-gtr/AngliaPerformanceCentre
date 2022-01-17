from django.contrib import admin
from .models import TeamMember


class TeamMemberAdmin(admin.ModelAdmin):
    list_display = [
        'first_name',
        'surname',
    ]


admin.site.register(TeamMember, TeamMemberAdmin)
