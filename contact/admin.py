from django.contrib import admin
from .models import Message, Callback, MessageResponse


class MessageAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'email',
        'message',
        'received_on',
    ]


class CallbackAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'phone',
        'received_on',
    ]


admin.site.register(Message, MessageAdmin)
admin.site.register(Callback, CallbackAdmin)
admin.site.register(MessageResponse)
