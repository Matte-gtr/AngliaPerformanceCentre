from django import forms
from captcha.fields import ReCaptchaField
from allauth.account.forms import SignupForm

from .models import Message, Callback, MessageResponse


class MessageForm(forms.ModelForm):
    captcha = ReCaptchaField()

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
            if field != 'captcha':
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
                self.fields[field].widget.attrs['class'] = 'form-control mb-1'


class CallbackForm(forms.ModelForm):
    class Meta:
        model = Callback
        fields = [
            'name',
            'phone',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'name': 'Name *',
            'phone': 'Contact Number *',
        }
        for field in self.fields:
            self.fields[field].label = ''
            if field != 'captcha':
                placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
                self.fields[field].widget.attrs['class'] = 'form-control mb-1'


class MessageResponseForm(forms.ModelForm):
    class Meta:
        model = MessageResponse
        fields = [
            'message_header',
            'message_body',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholders = {
            'message_header': 'Title *',
            'message_body': 'Message',
        }
        for field in self.fields:
            self.fields[field].label = ''
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'form-control mb-1'


class AllAuthSignupForm(SignupForm):
    captcha = ReCaptchaField()

    field_order = ['email', 'email2', 'username', 'password1',
                   'password2', 'captcha']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'captcha':
                self.fields[field].label = ''

    def save(self, request):
        user = super(AllAuthSignupForm, self).save(request)
        return user
