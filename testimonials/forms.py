from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'multiple': True
        })
    )

    class Meta:
        model = Review
        fields = [
            'stars',
            'review',
            'anon',
        ]
        labels = {
            'stars': 'Rating',
            'anon': 'Post as Anonymous',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['review'].widget.attrs['placeholder'] = 'Review'

        for field in self.fields:
            if field != 'anon':
                self.fields[field].widget.attrs['class'] = 'form-control mb-1'
                self.fields[field].label = ''
        self.fields['stars'].widget = forms.HiddenInput()
        self.fields['image'].widget.attrs['class'] = 'form-control bg-light-grey border-0 pl-0 text-white'
