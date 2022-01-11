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
        self.fields['review'].label = ''
        self.fields['image'].label = ''
        self.fields['stars'].label = ''

        for field in self.fields:
            if field != 'anon':
                self.fields[field].widget.attrs['class'] = 'form-control mb-1'
        self.fields['stars'].widget.attrs['class'] = 'd-none'
