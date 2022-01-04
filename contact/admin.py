from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'email',
        'message',
        'received_on',
    ]


admin.site.register(Message, MessageAdmin)
