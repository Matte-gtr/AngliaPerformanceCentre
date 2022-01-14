from django.db import models
from django.contrib.auth.models import User


class Review(models.Model):
    STAR_CHOICES = (
        ('','Select'),
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


class ReviewImage(models.Model):
    image = models.ImageField(upload_to="reviews", blank=True, null=True)

    def __str__(self):
        return str(self.pk)
