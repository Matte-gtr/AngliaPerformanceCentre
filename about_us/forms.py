from django import forms
from .models import TeamMember


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = [
            'first_name',
            'surname',
            'job',
            'image',
            'description',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field == "image":
                self.fields[field].widget.attrs['class'] = 'form-control mb-1\
                bg-trans border-0 text-white'
            else:
                self.fields[field].widget.attrs['class'] = 'form-control mb-1'
