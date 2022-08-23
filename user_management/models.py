from django.db import models
from django.contrib.auth.models import User


class UserOptions(models.Model):
    """ User options model set up for custom user options,
    intended for easy modification """
    email = models.OneToOneField(User, on_delete=models.CASCADE,
                                 related_name="user_options")
    update = models.BooleanField(default=False)
