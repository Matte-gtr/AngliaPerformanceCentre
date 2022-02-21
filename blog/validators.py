import os
from django.core.exceptions import ValidationError


def validate_video_file(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.mp4', '.mov', '.wmv', '.avi', '.webm', '.mpg',
                        '.mp2', '.mpeg', '.mpe', '.mpv', '.m4p', '.m4v',
                        '.qt', '.flv', '.swf', '.ogg', '.avchd']
    if not ext.lower() in valid_extensions:
        raise ValidationError(('You have selected an invalid video file' +
                               f' type: {ext}'), code='invalid-ft')
