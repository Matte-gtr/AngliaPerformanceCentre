from django import forms
from ckeditor_uploader.fields import RichTextUploadingField

from .models import BlogPost
from .validators import validate_video_file


class BlogPostForm(forms.ModelForm):
    post_body = RichTextUploadingField()
    video = forms.FileField(
        validators=[validate_video_file],
        required=False,
        widget=forms.ClearableFileInput(attrs={
            'multiple': True,
        })
    )
    videocontrol = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={
            'name': 'video_control',
            'id': 'id_video_control'
        })
    )

    class Meta:
        model = BlogPost
        fields = [
            'category',
            'post_title',
            'post_body',
            'header_image',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            if field != 'post_body':
                self.fields[field].widget.attrs['class'] = 'form-control mb-2'
            if field == 'header_image' or field == 'video':
                self.fields[field].widget.attrs['class'] = 'form-control \
                mb-2 border-0'
        self.fields['post_title'].widget.attrs['placeholder'] = "Title"
        self.fields['post_body'].label = ""
