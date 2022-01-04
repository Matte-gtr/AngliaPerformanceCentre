from django.db import models


class Message(models.Model):
    name = models.CharField(max_length=100, blank=False)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(max_length=254, blank=False)
    message = models.TextField(blank=False)
    received_on = models.DateTimeField(auto_now_add=True, blank=False)
    read = models.BooleanField(default=False)
    responded = models.BooleanField(default=False)

    def __str__(self):
        return self.name
