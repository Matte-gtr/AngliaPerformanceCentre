from django.db import models
from django.contrib.auth.models import User
from django.core.files import File

from io import BytesIO
from PIL import Image


class Review(models.Model):
    STAR_CHOICES = (
        ('', 'Select'),
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    )
    user = models.ForeignKey(User, related_name='reviews',
                             on_delete=models.RESTRICT)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(blank=True, null=True)
    stars = models.IntegerField(default='', choices=STAR_CHOICES, blank=False)
    review = models.TextField(blank=False)
    image = models.ManyToManyField('ReviewImage', blank=True)
    anon = models.BooleanField(default=False)
    read = models.BooleanField(default=False)
    authorised = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)


def compress(image):
    img = Image.open(image)
    img_io = BytesIO() 
    # img = img.resize([500,500])
    img = img.convert("RGB")
    img = img.save(img_io, 'JPEG', quality=70)
    new_image = File(img_io, name=image.name)
    return new_image


class ReviewImage(models.Model):
    image = models.ImageField(upload_to="reviews", blank=True, null=True)

    def __str__(self):
        return str(self.pk)

    def save(self, *args, **kwargs):
        if self.image:
            if self.image.size > (300 * 1024):
                new_image = compress(self.image)
                self.image = new_image
        super().save(*args, **kwargs)
