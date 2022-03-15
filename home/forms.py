from django import forms

from .models import Advert


class AdvertForm(forms.ModelForm):
    class Meta:
        model = Advert
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control mb-2'

        self.fields['image'].widget.attrs = {
            'class': 'form-control-file mb-2 bg-trans border-0 pl-0 \
                text-white',
            }
