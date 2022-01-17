from django.db import models


class TeamMember(models.Model):
    first_name = models.CharField(max_length=40, blank=False)
    surname = models.CharField(max_length=40, blank=False)
    job = models.CharField(max_length=120, blank=False)
    image = models.ImageField(upload_to="team", blank=True, null=True)
    description = models.TextField(blank=False)
    added_on = models.DateTimeField(auto_now_add=True)
    order = models.IntegerField()

    def __str__(self):
        return f'{self.first_name} {self.surname}'
