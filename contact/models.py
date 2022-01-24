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
        return str(self.name)


class Callback(models.Model):
    name = models.CharField(max_length=100, blank=False)
    phone = models.CharField(max_length=20, blank=False)
    received_on = models.DateTimeField(auto_now_add=True, blank=False)
    read = models.BooleanField(default=False)
    responded = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


class MessageResponse(models.Model):
    message_header = models.CharField(max_length=100, blank=False)
    message_body = models.TextField(blank=False)
    response_to = models.ForeignKey("Message", blank=False, null=True,
                                    on_delete=models.CASCADE,
                                    related_name="responses")
    sent_on = models.DateTimeField(auto_now_add=True, blank=False)

    def __str__(self):
        return str(self.pk)
