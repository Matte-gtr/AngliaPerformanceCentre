from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'multiple': True,
        })
    )
    imagecontrol = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={
            'name': 'image_control',
            'id': 'id_image_control'
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
        self.fields['image'].widget.attrs = {
            'class': 'form-control bg-trans border-0 pl-0 text-white',
            'id': 'image-select',
            'multiple': True,
            }
