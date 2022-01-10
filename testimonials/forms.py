from django import forms
from .models import Review, ReviewImages


class ReviewForm(forms.ModelForm):
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
        self.fields['stars'].label = 'Ratings'

        for field in self.fields:
            if field != 'anon':
                self.fields[field].widget.attrs['class'] = 'form-control mb-1'


class ReviewImagesForm(forms.ModelForm):
    class Meta:
        model = ReviewImages
        fields = [
            'image',
        ]
        labels = {
            'image': 'Image',
        }
