from django.db import models
from django.contrib.auth.models import User


class UserOptions(models.Model):
    """ User options model set up for custom user options,
    intended for easy modification """
    email = models.OneToOneField(User, on_delete=models.CASCADE,
                                 related_name="user_options")
    update = models.BooleanField(default=False)


class VehicleBooking(models.Model):
    registration = models.CharField(max_length=20, blank=False, null=False)
    work_type = models.CharField(max_length=256, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name="bookings")
    date = models.DateField(blank=False, null=False)
    time = models.TimeField(blank=False, null=False)
    duration = models.DecimalField(decimal_places=1, blank=False, null=False,
                                   max_digits=5)
