from django import forms
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = [
            'name',
            'phone',
            'email',
            'message',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Name *',
            'phone': 'Contact Number',
            'email': 'Email Address *',
            'message': 'Message *',
        }
        for field in self.fields:
            self.fields[field].label = ''
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control mb-1'
