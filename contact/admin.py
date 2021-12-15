from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'email',
        'message',
    ]


admin.site.register(Message, MessageAdmin)
