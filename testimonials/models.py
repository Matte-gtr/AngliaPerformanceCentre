from django.db import models
from django.contrib.auth.models import User


class Review(models.Model):
    STAR_CHOICES = (
        (1, 'Very Poor'),
        (2, 'Poor'),
        (3, 'Average'),
        (4, 'Good'),
        (5, 'Very Good'),
    )
    user = models.ForeignKey(User, related_name='reviews',
                             on_delete=models.RESTRICT)
    created_on = models.DateTimeField(auto_now_add=True)
    stars = models.IntegerField(default=3, choices=STAR_CHOICES)
    review = models.TextField(blank=False)
    image = models.ManyToManyField('ReviewImage', blank=True)
    anon = models.BooleanField(default=False)
    authorised = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)


class ReviewImage(models.Model):
    image = models.ImageField(upload_to="reviews", blank=True, null=True)

    def __str__(self):
        return str(self.pk)
